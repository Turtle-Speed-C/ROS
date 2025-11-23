#include <QApplication> //Qt应用程序的核心
#include <QLabel>       //标签控件，用于显示文本或图片
#include <QString>      //Qt的字符串类
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/system_status.hpp>

using SystemStatus = status_interfaces::msg::SystemStatus;

class SysStatusDisplay : public rclcpp::Node
{
public:
    SysStatusDisplay() : Node("sys_status_display")
    {
        subscription_ = this->create_subscription<SystemStatus>(
            "sys_status", // 订阅的话题名
            10,           // 最多十条消息
            [&](const SystemStatus::SharedPtr msg) -> void
            { label_->setText(get_qstr_from_msg(msg)); });
        // setText 是把文本设置在标签上
        // 在这里是把msg通过 get_qstr_from_msg 之后放在标签上。

        label_ = new QLabel(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        // 创建一个QLabel*类型的标签，标签的内容是get_qstr_from_msg(std::make_shared<SystemStatus>())
        // 为什么这里要用只能指针，因为get_qstr_from_msg参数就是只能指针，为什么参数是智能指针，因为
        label_->show();
        // 把标签显示在屏幕上
    }

    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str
            << "=========== 系统状态可视化显示工具 ============\n"
            << " 数 据 时 间 :\t" << msg->stamp.sec << "\ts\n"
            << " 用 户 名 :\t" << msg->host_name << "\t\n"
            << " CPU 使用率 :\t" << msg->cpu_percent << "\t%\n"
            << " 内存使用率 :\t" << msg->memory_percent << "\t%\n"
            << " 内存总大小 :\t" << msg->memory_total << "\tMB\n"
            << " 剩余有效内存 :\t" << msg->memory_available << "\tMB\n"
            << " 网络发送量 :\t" << msg->net_sent << "\tMB\n"
            << " 网络接收量 :\t" << msg->net_recv << "\tMB\n"
            << "==========================================";
        return QString::fromStdString(show_str.str());
        // show_str.str()是把字符流川化为std::string
        // fromStdString又把std：：string转化为QString
    }

private:
    rclcpp::Subscription<SystemStatus>::SharedPtr subscription_;
    QLabel *label_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);
    auto node = std::make_shared<SysStatusDisplay>();
    std::thread spin_thread([&]() -> void
                            { rclcpp::spin(node); });
    spin_thread.detach();
    app.exec();
    rclcpp::shutdown();
    return 0;
}
