// Lambda表达式
//[capture list]（parameters） -＞ return_type { function body }
#include <iostream>
#include <algorithm>

int main()
{
    auto add = [](int a, int b) -> int
    { return a + b; };
    auto sum = add(5, 15);

    auto print_sum = [sum]() -> void
    { std::cout << "5+15=" << sum << std::endl; };
    print_sum();

    return 0;
}