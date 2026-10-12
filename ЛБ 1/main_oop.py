import sys
import math


class CoefficientReader:
    def __init__(self, args):
        self.args = args

    @staticmethod
    def is_valid(value) -> bool:
        try:
            return math.isfinite(float(value))
        except (TypeError, ValueError):
            return False

    def read(self, index, name):
        if len(self.args) > index and self.is_valid(self.args[index]):
            return float(self.args[index])
        while True:
            val = input(f"Введите коэффициент {name}: ").strip()
            if self.is_valid(val):
                return float(val)
            print("Ошибка ввода. Повторите попытку.")


class BiquadraticEquation:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
        self.infinite = False

    def __str__(self):
        return f"{self.a}*x^4 + ({self.b})*x^2 + ({self.c}) = 0"

    def _roots_y(self):
        if self.a == 0:
            if self.b == 0:
                self.infinite = self.c == 0
                return []
            return [-self.c / self.b]
        d = self.b * self.b - 4 * self.a * self.c
        if d < 0: return []
        if d == 0: return [-self.b / (2 * self.a)]
        sqrt_d = math.sqrt(d)
        return [(-self.b + sqrt_d) / (2 * self.a), (-self.b - sqrt_d) / (2 * self.a)]

    def roots(self):
        self.infinite = False
        x_roots = set()
        for y in self._roots_y():
            if y > 0:
                r = math.sqrt(y)
                x_roots.update((r, -r))
            elif y == 0:
                x_roots.add(0.0)
        return sorted(x_roots)


class BiquadraticApp:
    def __init__(self, args):
        self.reader = CoefficientReader(args)

    def run(self):
        print("=== Решение биквадратного уравнения (ООП) ===\n")
        eq = BiquadraticEquation(
            self.reader.read(0, "A"),
            self.reader.read(1, "B"),
            self.reader.read(2, "C")
        )

        print(f"\nУравнение: {eq}")
        roots = eq.roots()

        if eq.infinite:
            print("Корень — любое действительное число.")
        elif not roots:
            print("Действительных корней нет.")
        else:
            print("Корни:")
            for i, x in enumerate(roots, start=1):
                print(f"  x{i} = {x}")


if __name__ == "__main__":
    BiquadraticApp(sys.argv[1:]).run()