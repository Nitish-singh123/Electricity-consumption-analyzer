"""
Test suite - Electricity Consumption Analyzer.

Run with:  python -m unittest -v

Covers the FSM transitions, the functional pipeline, the SymPy calculations,
the real TCP client/server integration and invalid-input handling.
"""

import json
import os
import socket
import threading
import unittest

import client
import server

DATASET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.csv")


class FSMTests(unittest.TestCase):
    """FSM input bands, transitions and state paths."""

    def test_input_band_boundaries(self):
        self.assertEqual(server.band(9.9), "LT10")
        self.assertEqual(server.band(10), "B10_19")
        self.assertEqual(server.band(19.9), "B10_19")
        self.assertEqual(server.band(20), "B20_29")
        self.assertEqual(server.band(29.9), "B20_29")
        self.assertEqual(server.band(30), "GE30")
        self.assertEqual(server.band(1000), "GE30")

    def test_transition_boundaries(self):
        self.assertEqual(server.fsm_next("LOW", 9), "LOW")
        self.assertEqual(server.fsm_next("LOW", 10), "MODERATE")
        self.assertEqual(server.fsm_next("MODERATE", 20), "HIGH")
        self.assertEqual(server.fsm_next("HIGH", 30), "OVERLOAD")
        self.assertEqual(server.fsm_next("OVERLOAD", 5), "LOW")

    def test_transition_table_is_complete(self):
        self.assertEqual(len(server.TRANSITIONS), 16)  # 4 states x 4 input bands

    def test_fsm_path_for_rising_usage(self):
        self.assertEqual(
            server.walk_fsm("LOW", [12, 18, 26]),
            ["LOW", "MODERATE", "MODERATE", "HIGH"],
        )


class FunctionalProgrammingTests(unittest.TestCase):
    """Higher-order functions, closures, map, filter and reduce."""

    def test_default_tou_closure(self):
        self.assertEqual(server.TOU_BILL(8.0, 4.0), 40.0)  # 8 x 4 + 4 x 2

    def test_closure_with_custom_rates(self):
        calculator = server.make_bill_calculator(5.0, 3.0)
        self.assertEqual(calculator(8.0, 4.0), 52.0)
        self.assertEqual(calculator.peak_rate, 5.0)

    def test_map_enrich_does_not_mutate_input(self):
        record = {"customer_id": "C01", "day_index": 1, "peak_units": 8.0, "offpeak_units": 4.0}
        enriched = server.enrich(record)
        self.assertEqual(enriched["total_units"], 12.0)
        self.assertEqual(enriched["tou_bill"], 40.0)
        self.assertNotIn("total_units", record)

    def test_filter_and_reduce_pipeline(self):
        records = client.load_dataset(DATASET)
        analysis = server.analyze_records(records)
        manual_units = sum(r["peak_units"] + r["offpeak_units"] for r in records)
        manual_high = sum(
            1 for r in records if (r["peak_units"] + r["offpeak_units"]) >= 20.0
        )
        self.assertEqual(analysis["summary"]["total_units"], round(manual_units, 2))
        self.assertEqual(analysis["summary"]["total_units"], 223.0)
        self.assertEqual(len(analysis["high_usage_records"]), manual_high)
        self.assertEqual(len(analysis["high_usage_records"]), 4)


class SymPyTests(unittest.TestCase):
    """Symbolic tariff, trend fit and budget solve."""

    def test_slab_bill(self):
        self.assertEqual(server.bill_amount(12), 36.0)
        self.assertEqual(server.bill_amount(50), 150.0)
        self.assertEqual(server.bill_amount(60), 200.0)

    def test_trend_fit_and_prediction(self):
        a_value, b_value = server.fit_trend([12, 18, 26])
        self.assertAlmostEqual(a_value, 7.0, places=6)
        self.assertAlmostEqual(b_value, 14.0 / 3.0, places=6)
        self.assertAlmostEqual(server.predict_day(a_value, b_value, 4), 32.67, places=2)

    def test_budget_break_even_solve(self):
        self.assertEqual(server.budget_units(150), 50.0)
        self.assertEqual(server.budget_units(200), 60.0)
        self.assertAlmostEqual(server.budget_units(100), 100.0 / 3.0, places=2)

    def test_trend_equation_sign_formatting(self):
        rising = [
            {"customer_id": "T1", "customer_name": "Rise", "day_index": day,
             "peak_units": units, "offpeak_units": 0.0}
            for day, units in ((1, 12.0), (2, 18.0), (3, 26.0))
        ]
        self.assertEqual(
            server.analyze_records(rising)["customers"][0]["trend_equation"],
            "y = 7.0000x + 4.6667",
        )

        falling = [
            {"customer_id": "T2", "customer_name": "Fall", "day_index": day,
             "peak_units": units, "offpeak_units": 0.0}
            for day, units in ((1, 0.0), (2, 17.0), (3, 25.0))
        ]
        self.assertEqual(
            server.analyze_records(falling)["customers"][0]["trend_equation"],
            "y = 12.5000x - 11.0000",
        )


class IntegrationTests(unittest.TestCase):
    """Real TCP communication between the client and the server."""

    @classmethod
    def setUpClass(cls):
        cls.server_socket = server.create_server_socket("127.0.0.1", 0)
        cls.port = cls.server_socket.getsockname()[1]
        cls.worker = threading.Thread(
            target=server.serve,
            kwargs={"server_socket": cls.server_socket, "verbose": False},
            daemon=True,
        )
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.server_socket.close()
        cls.worker.join(timeout=5)

    def test_end_to_end_analysis(self):
        records = client.load_dataset(DATASET)
        analysis = client.send_records("127.0.0.1", self.port, records)
        self.assertEqual(analysis["records_analyzed"], 12)
        self.assertEqual(analysis["summary"]["customers"], 4)
        self.assertEqual(analysis["customers"][0]["customer_id"], "C03")
        self.assertEqual(analysis["customers"][0]["final_state"], "OVERLOAD")
        self.assertEqual(analysis["budget"]["max_units_allowed"], 120.0)

    def test_server_refuses_double_bind(self):
        self.assertTrue(server.port_in_use("127.0.0.1", self.port))
        with self.assertRaises(SystemExit):
            server.create_server_socket("127.0.0.1", self.port)

    def test_malformed_json_is_rejected_gracefully(self):
        with socket.create_connection(("127.0.0.1", self.port), timeout=5) as connection:
            connection.sendall(b"this is not json\n")
            buffer = b""
            while not buffer.endswith(b"\n"):
                chunk = connection.recv(4096)
                if not chunk:
                    break
                buffer += chunk
        self.assertIn("JSONDecodeError", json.loads(buffer.decode("utf-8"))["error"])


class EdgeCaseTests(unittest.TestCase):
    """Invalid records and single-day consumers."""

    def test_invalid_records_are_reported_not_crashing(self):
        records = [
            {"customer_id": "X1", "customer_name": "Test", "day_index": 1,
             "peak_units": -5.0, "offpeak_units": 2.0},
            {"customer_id": "X2", "customer_name": "Test", "day_index": 1,
             "peak_units": 3.0, "offpeak_units": 1.0},
            {"customer_id": "X3"},
        ]
        analysis = server.analyze_records(records)
        self.assertEqual(analysis["records_analyzed"], 1)
        self.assertEqual(analysis["records_invalid"], 2)
        self.assertEqual(analysis["summary"]["total_units"], 4.0)

    def test_single_day_consumer(self):
        records = [{"customer_id": "X9", "customer_name": "Solo", "day_index": 1,
                    "peak_units": 5.0, "offpeak_units": 5.0}]
        customer = server.analyze_records(records)["customers"][0]
        self.assertEqual(customer["fsm_path"], ["LOW", "MODERATE"])
        self.assertEqual(customer["predicted_next_day_units"], 10.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
