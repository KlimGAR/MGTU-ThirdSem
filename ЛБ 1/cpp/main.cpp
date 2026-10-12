#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#endif

std::string trim(const std::string &s) {
    size_t begin = s.find_first_not_of(" \t\r\n");
    if (begin == std::string::npos) return "";
    return s.substr(begin, s.find_last_not_of(" \t\r\n") - begin + 1);
}

bool tryParse(const std::string &raw, double &result) {
    std::string s = trim(raw);
    if (s.empty()) return false;
    try {
        size_t pos = 0;
        double value = std::stod(s, &pos);
        if (pos != s.size() || !std::isfinite(value)) return false;
        result = value;
        return true;
    } catch (...) {
        return false;
    }
}

double readFromKeyboard(const std::string &name) {
    std::string line;
    double value;
    while (true) {
        std::cout << "Введите коэффициент " << name << ": ";
        if (!std::getline(std::cin, line)) std::exit(1);
        if (tryParse(line, value)) return value;
        std::cout << "Ошибка ввода. Повторите попытку.\n";
    }
}

double getCoefficient(int argc, char *argv[], int index, const std::string &name) {
    if (argc > index) {
        double value;
        if (tryParse(argv[index], value)) return value;
    }
    return readFromKeyboard(name);
}

std::vector<double> solveQuadratic(double a, double b, double c) {
    double d = b * b - 4 * a * c;
    if (d < 0) return {};
    if (d == 0) return {-b / (2 * a)};
    double sqrtD = std::sqrt(d);
    return {(-b + sqrtD) / (2 * a), (-b - sqrtD) / (2 * a)};
}

std::vector<double> solveBiquadratic(double a, double b, double c, bool &infinite) {
    infinite = false;
    std::vector<double> yRoots;
    if (a == 0) {
        if (b == 0) {
            infinite = (c == 0);
            return {};
        }
        yRoots.push_back(-c / b);
    } else {
        yRoots = solveQuadratic(a, b, c);
    }

    std::vector<double> xRoots;
    for (double y : yRoots) {
        if (y > 0) {
            double r = std::sqrt(y);
            xRoots.push_back(r);
            xRoots.push_back(-r);
        } else if (y == 0) {
            xRoots.push_back(0.0);
        }
    }
    std::sort(xRoots.begin(), xRoots.end());
    xRoots.erase(std::unique(xRoots.begin(), xRoots.end()), xRoots.end());
    return xRoots;
}

int main(int argc, char *argv[]) {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
    std::cout << "=== Решение биквадратного уравнения ===\n\n";

    double a = getCoefficient(argc, argv, 1, "A");
    double b = getCoefficient(argc, argv, 2, "B");
    double c = getCoefficient(argc, argv, 3, "C");

    std::cout << "\nУравнение: " << a << "*x^4 + (" << b << ")*x^2 + (" << c << ") = 0\n";

    bool infinite;
    std::vector<double> roots = solveBiquadratic(a, b, c, infinite);
    
    if (infinite) {
        std::cout << "Корень — любое действительное число.\n";
    } else if (roots.empty()) {
        std::cout << "Действительных корней нет.\n";
    } else {
        std::cout << "Корни:\n";
        for (size_t i = 0; i < roots.size(); ++i) {
            std::cout << "  x" << i + 1 << " = " << roots[i] << "\n";
        }
    }
    return 0;
}