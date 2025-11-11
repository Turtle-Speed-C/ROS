import rclpy
from rclpy.node import Node
from python_pkg.person_node import PersonNode

class WriterNode(PersonNode):
    def __init__(self,node_name:str, name:str,age:int)->None:
        super().__init__(node_name,name,age)
        print('WriteNode的__init__方法被调用了')

    def write(self, book:str):
        self.book=book
        self.get_logger().info(f'我写的书是{self.book}')

def main():
    rclpy.init()
    node=WriterNode('writer_node','lxf',24)
    node.write('python_study')
    rclpy.spin(node)
    rclpy.shutdown()