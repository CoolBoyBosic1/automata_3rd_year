#include <iostream>

int main() {
    int n = 10;

    for (int i = 0; i < n; ++i) {
        if (i == 5) {
            break;
        }
    }

    int j = 0;
    while (j < n) {
        ++j;
        if (j % 2 == 0) {
            continue;
        }
    }


    int k = 0;
    while (k < n) {
        for (int t = 0; t < 3; ++t) {
            if (t == 1) {
                break;  
            }
        }
        ++k;
    }

    int p = 0;
    do {
        if (p > 3) {
            break;
        }
        ++p;
    } while (p < 10);

    for (int x = 0; x < 5; ++x) {
        switch (x) {
            case 1:
                std::cout << "one\n";
                break;
            case 2:
                std::cout << "two\n";
                break;
            default:
                break;
        }
    }

    return 0;
}
