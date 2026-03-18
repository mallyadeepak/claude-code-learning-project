# Test Skill

Run the project's test suite and report results.

## Arguments
- `$ARGUMENTS` - Optional: specific test file or test name pattern

## Instructions

1. Run pytest with verbose output:
   - No arguments: `pytest tests/ -v`
   - With arguments: `pytest tests/ -v -k "$ARGUMENTS"`
2. Analyze the test results
3. Report:
   - Total tests run
   - Tests passed
   - Tests failed (with failure details)
   - Test coverage if available
4. If tests fail, suggest fixes based on the error messages

## Example Usage
```
/test
/test test_add_task
/test "test_task"
```

## Example Output
```
## Test Results

Ran 5 tests in 0.23s

**Passed:** 5
**Failed:** 0

All tests passing!
```
