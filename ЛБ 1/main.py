import sys
import math


def is_valid(value: str) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def get_coefficient(args, index, name):
    if len(args) > index and is_valid(args[index]):
        return float(args[index])
    while True:
        val = input(f"Введите коэффициент {name}: ").strip()
        if is_valid(val):
            return float(val)
        print("Ошибка ввода. Повторите попытку.")


def solve_quadratic(a, b, c):
    d = b * b - 4 * a * c
    if d < 0: return []
    if d == 0: return [-b / (2 * a)]
    sqrt_d = math.sqrt(d)
    return [(-b + sqrt_d) / (2 * a), (-b - sqrt_d) / (2 * a)]


def solve_biquadratic(a, b, c):
    if a == 0:
        if b == 0: return [], c == 0
        y_roots = [-c / b]
    else:
        y_roots = solve_quadratic(a, b, c)

    x_roots = set()
    for y in y_roots:
        if y > 0:
            r = math.sqrt(y)
            x_roots.update((r, -r))
        elif y == 0:
            x_roots.add(0.0)
    return sorted(x_roots), False


def main():
    args = sys.argv[1:]
    print("=== Решение биквадратного уравнения ===\n")

    a = get_coefficient(args, 0, "A")
    b = get_coefficient(args, 1, "B")
    c = get_coefficient(args, 2, "C")

    print(f"\nУравнение: {a}*x^4 + ({b})*x^2 + ({c}) = 0")

    roots, infinite = solve_biquadratic(a, b, c)

    if infinite:
        print("Корень — любое действительное число.")
    elif not roots:
        print("Действительных корней нет.")
    else:
        print("Корни:")
        for i, x in enumerate(roots, start=1):
            print(f"  x{i} = {x}")


if __name__ == "__main__":
    main()