from __future__ import annotations

import argparse
from pathlib import Path

from app.graph import ShoppingAssistant


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Student scaffold CLI.")
    parser.add_argument("--question", help="Run one question through the graph.")
    parser.add_argument("--test-file", default="data/test.json")
    parser.add_argument("--trace-file", default=None)
    parser.add_argument("--batch", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    assistant = ShoppingAssistant()

    if args.batch:
        test_file_path = Path(args.test_file)
        from datetime import datetime
        now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_dir = Path("src/artifacts/traces") / f"batch-{now_str}"
        print(f"Starting batch test using {test_file_path}...")
        print(f"Traces will be stored in {output_dir}")
        summary = assistant.run_batch(
            test_file=test_file_path,
            output_dir=output_dir,
            rebuild_index=False
        )
        print("\n--- BATCH RUN SUMMARY ---")
        print(f"Total Cases:  {summary['total_cases']}")
        print(f"Passed Cases: {summary['passed_cases']}")
        print(f"Failed Cases: {summary['failed_cases']}")
        print(f"Pass Rate:    {summary['pass_rate']:.2%}")
        if summary['failed_cases'] > 0:
            print("\nFailed Cases Details:")
            for case in summary['cases']:
                if not case['passed']:
                    print(f"- {case['id']}: '{case['question']}'")
                    print(f"  Expected: Route={case['expected_route']}, Status={case['expected_status']}")
                    print(f"  Actual:   Route={case['actual_route']}, Status={case['actual_status']}")
                    print(f"  Route Pass: {case['route_pass']}, Status Pass: {case['status_pass']}, Contains Pass: {case['contains_pass']}")
    elif args.question:
        trace_path = Path(args.trace_file) if args.trace_file else None
        res = assistant.ask(args.question, trace_file=trace_path)
        print("\n--- FINAL ANSWER ---")
        print(res["final_answer"])
        print("\n--- ROUTE INFO ---")
        print(f"Route:  {res['route']}")
        print(f"Status: {res['status']}")
    else:
        print("Please provide --question or --batch to run the assistant.")


if __name__ == "__main__":
    main()
