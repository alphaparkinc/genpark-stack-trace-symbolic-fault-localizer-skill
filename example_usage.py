"""
Example usage of Stack Trace Symbolic Fault Localizer Skill.
"""

from client import FaultLocalizer


def main():
    print("=== Stack Trace Symbolic Fault Localizer Demonstration ===")
    localizer = FaultLocalizer()

    sample_traceback = """
Traceback (most recent call last):
  File "app/main.py", line 42, in handle_request
    result = orchestrate_agent(user_input)
  File "app/core/orchestrator.py", line 108, in orchestrate_agent
    plan = planner.generate_dag(query)
  File "app/core/planner.py", line 55, in generate_dag
    nodes = [parse_node(t) for t in raw_tokens]
  File "app/core/planner.py", line 23, in parse_node
    return Node(id=t["id"], action=t["action"])
KeyError: 'action'
"""

    res = localizer.parse_traceback(sample_traceback)
    print("Exception Type:   ", res["exception_type"])
    print("Exception Message:", res["exception_message"])
    print("Call Depth:       ", res["frame_depth"], "frames")
    print("\nProbable Root Cause Frame:")
    rc = res["probable_root_cause"]
    print(f"  File: {rc['file']} (line {rc['line']})")
    print(f"  Function: {rc['function']}")
    print(f"  Code: {rc['code']}")

    # Calculate Ochiai suspiciousness
    ochiai = localizer.compute_ochiai_suspiciousness(line_hits_failed=5, line_hits_passed=1, total_failed=5)
    print(f"\nOchiai Fault Suspiciousness Score: {ochiai} (High probability of true bug)")


if __name__ == "__main__":
    main()
