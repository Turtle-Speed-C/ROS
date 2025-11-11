// #include "rclcpp/rclcpp.hpp"
#include "iostream"

int main(int argc,char **argv)
{
    std::cout<<"参数数量="<<argc<<std::endl;
    std::cout<<"程序名字="<<argv[0]<<std::endl;
    std::string arg0=argv[0];

    if(arg0=="lxf"){
        std::cout<<"this is lxf"<<std::endl;
    }

    return 0;
}