#!/bin/bash

# MarketMind Test Runner
# This script helps run tests with common configurations

echo "🧪 MarketMind Test Suite"
echo "========================"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest is not installed!"
    echo "Install it with: pip install -r requirements-dev.txt"
    exit 1
fi

# Parse arguments
case "$1" in
    "cov"|"coverage")
        echo "📊 Running tests with coverage..."
        pytest --cov=src --cov-report=html --cov-report=term-missing
        echo ""
        echo "✅ Coverage report generated in htmlcov/index.html"
        ;;
    "unit")
        echo "🔬 Running unit tests..."
        pytest -m unit -v
        ;;
    "fast")
        echo "⚡ Running tests (fast mode, no coverage)..."
        pytest -v
        ;;
    "file")
        if [ -z "$2" ]; then
            echo "❌ Please specify a test file"
            echo "Usage: ./run_tests.sh file tests/test_api.py"
            exit 1
        fi
        echo "📝 Running tests from $2..."
        pytest "$2" -v
        ;;
    "verbose"|"-v")
        echo "📢 Running tests with verbose output..."
        pytest -vv
        ;;
    "help"|"-h"|"--help")
        echo "Usage: ./run_tests.sh [option]"
        echo ""
        echo "Options:"
        echo "  (none)        Run all tests"
        echo "  cov           Run with coverage report"
        echo "  unit          Run only unit tests"
        echo "  fast          Run without coverage (faster)"
        echo "  file <path>   Run specific test file"
        echo "  verbose       Run with verbose output"
        echo "  help          Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh"
        echo "  ./run_tests.sh cov"
        echo "  ./run_tests.sh file tests/test_api.py"
        ;;
    "")
        echo "▶️  Running all tests..."
        pytest -v
        ;;
    *)
        echo "❌ Unknown option: $1"
        echo "Run './run_tests.sh help' for usage information"
        exit 1
        ;;
esac

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "❌ Some tests failed (exit code: $exit_code)"
fi

exit $exit_code
