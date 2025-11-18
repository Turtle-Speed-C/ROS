#include <QApplication> //Qt应用程序的核心
#include <QLabel>       //标签控件，用于显示文本或图片
#include <QString>      //Qt的字符串类

int main(int argc, char **argv)
{
    QApplication app(argc, argv);   //创建一个应用程序对象
    QLabel *label = new QLabel();   //创建一个标签控件指针，new：动态分配内存，创建一个新的QLabel对象，这个标签将用来显示文本
    QString message = QString::fromStdString("李晓凡，你终究会成功!");
    //将标准C++字符串"Hello Qt!"转换为Qt的QString类型
    //fromStdString()：转换函数，将std::string转换为QString
    label->setText(message);
    // setText()：将文本设置到标签上
    label->show();
    //使标签控件显示在屏幕上
    //调用后，一个包含"Hello Qt!"文本的窗口会弹出
    app.exec();
    // 启动Qt的事件循环
    return 0;
}
