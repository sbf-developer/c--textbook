#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${ROOT}/build/example-verification"
MODE="${1:-full}"
CXX="${CXX:-g++}"

mkdir -p "${BUILD_DIR}"

if ! command -v "${CXX}" >/dev/null 2>&1; then
    echo "compiler not found: ${CXX}" >&2
    exit 2
fi

FLAGS=(-std=c++23 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -pthread)
count=0
for source in "${ROOT}"/examples/*.cpp "${ROOT}"/examples/chapters/ch*.cpp; do
    [[ -f "${source}" ]] || continue
    name="$(basename "${source}" .cpp)"
    "${CXX}" "${FLAGS[@]}" "${source}" -o "${BUILD_DIR}/${name}"
    count=$((count + 1))
done

if [[ "${MODE}" != "--compile-only" ]]; then
    "${BUILD_DIR}/calculator" >/dev/null
    "${BUILD_DIR}/text_analysis" >/dev/null
    "${BUILD_DIR}/task_manager" >/dev/null
    "${BUILD_DIR}/ownership" >/dev/null
    "${BUILD_DIR}/polymorphism" >/dev/null
    "${BUILD_DIR}/algorithms" >/dev/null
    "${BUILD_DIR}/concepts" >/dev/null
    "${BUILD_DIR}/graph" >/dev/null
    "${BUILD_DIR}/concurrency" | grep -qx '4000'
    "${BUILD_DIR}/expected_style" >/dev/null
fi

echo "verified ${count} standalone C++23 translation units with ${CXX}"

