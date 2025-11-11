#include <iostream>
#include <functional>

void save_with_free_fun(const std::string &file_name)
{
    std::cout << "调用了自由函数，保存" << file_name << std::endl;
};

class FileSave
{
public:
    void save_with_member_fun(const std::string &file_name)
    {
        std::cout << "调用了成员函数，保存" << file_name << std::endl;
    };
};

int main()
{
    FileSave file_save;
    auto save_with_lambda_fun = [](const std::string &file_name)
    {
        std::cout << "调用了lambda函数，保存" << file_name << std::endl;
    };

    // std::function<返回类型(参数类型1, 参数类型2, ...)>
    // std::function<void(int, int)> func;  // 接受两个int参数，返回void的函数
    // std::function<int(double)> calc;     // 接受double参数，返回int的函数

    // std::bind是一个模板函数，用于绑定函数和参数，返回一个函数对象：
    // auto newCallable = std::bind(func, arg1, arg2, ..., argN);

    // 将自由函数放进function对象中
    std::function<void(const std::string &)> save1 = save_with_free_fun;
    // 将成员放进function对象中
    std::function<void(const std::string &)> save2 = std::bind(&FileSave::save_with_member_fun, &file_save, std::placeholders::_1);
    // 将Lambda函数放进function对象中
    std::function<void(const std::string &)> save3 = save_with_lambda_fun;

    save1("file.txt");
    save2("file.txt");
    save3("file.txt");

    return 0;
}