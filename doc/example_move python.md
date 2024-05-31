- het uitvoeren van het python example_walk script krijg ik de error:
Traceback (most recent call last):

  File "/home/gert/unitree_legged_sdk/python_scripts/test.py", line 8, in <module>

    import robot_interface as sdk

ModuleNotFoundError: No module named 'robot_interface'


- Op deze forum zie ik hetzelfde probleem staan, maar ik zie niet de oplossing.
https://github.com/unitreerobotics/unitree_legged_sdk/issues/46


- Ik probeer nu de missende module te installeren volgens volgende guide: https://roboticsyy.github.io/robot_interface/

cmake .. lukt, bij make krijg ik volgende error:

gert@gert-VirtualBox:~/ur_modern_driver/libur_modern_driver/build$ make

[ 11%] Building CXX object CMakeFiles/ur_driver_lib.dir/src/tcp_socket.cpp.o

[ 22%] Building CXX object CMakeFiles/ur_driver_lib.dir/src/commander.cpp.o

[ 33%] Building CXX object CMakeFiles/ur_driver_lib.dir/src/master_board.cpp.o

In file included from /home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/state.h:25,

                 from /home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/master_board.h:26,

                 from /home/gert/ur_modern_driver/libur_modern_driver/src/master_board.cpp:19:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/pipeline.h:48:24: error: ‘shared_ptr’ has not been declared

   48 |   virtual bool consume(shared_ptr<T> product) = 0;

      |                        ^~~~~~~~~~

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/pipeline.h:48:34: error: expected ‘,’ or ‘...’ before ‘<’ token

   48 |   virtual bool consume(shared_ptr<T> product) = 0;

      |                                  ^

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/pipeline.h:91:16: error: ‘shared_ptr’ has not been declared

   91 |   bool consume(shared_ptr<T> product)

      |                ^~~~~~~~~~

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/pipeline.h:91:26: error: expected ‘,’ or ‘...’ before ‘<’ token

   91 |   bool consume(shared_ptr<T> product)

      |                          ^

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/pipeline.h: In member function ‘bool MultiConsumer<T>::consume(int)’:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/pipeline.h:96:25: error: ‘product’ was not declared in this scope

   96 |       if (!con->consume(product))

      |                         ^~~~~~~

In file included from /home/gert/ur_modern_driver/libur_modern_driver/src/master_board.cpp:20:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h: At global scope:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:31:24: error: ‘shared_ptr’ has not been declared

   31 |   virtual bool consume(shared_ptr<RTPacket> packet)

      |                        ^~~~~~~~~~

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:31:34: error: expected ‘,’ or ‘...’ before ‘<’ token

   31 |   virtual bool consume(shared_ptr<RTPacket> packet)

      |                                  ^

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h: In member function ‘virtual bool URRTPacketConsumer::consume(int)’:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:33:12: error: ‘packet’ was not declared in this scope; did you mean ‘RTPacket’?

   33 |     return packet->consumeWith(*this);

      |            ^~~~~~

      |            RTPacket

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h: At global scope:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:45:24: error: ‘shared_ptr’ has not been declared

   45 |   virtual bool consume(shared_ptr<StatePacket> packet)

      |                        ^~~~~~~~~~

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:45:34: error: expected ‘,’ or ‘...’ before ‘<’ token

   45 |   virtual bool consume(shared_ptr<StatePacket> packet)

      |                                  ^

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h: In member function ‘virtual bool URStatePacketConsumer::consume(int)’:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:47:12: error: ‘packet’ was not declared in this scope; did you mean ‘RTPacket’?

   47 |     return packet->consumeWith(*this);

      |            ^~~~~~

      |            RTPacket

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h: At global scope:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:62:24: error: ‘shared_ptr’ has not been declared

   62 |   virtual bool consume(shared_ptr<MessagePacket> packet)

      |                        ^~~~~~~~~~

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:62:34: error: expected ‘,’ or ‘...’ before ‘<’ token

   62 |   virtual bool consume(shared_ptr<MessagePacket> packet)

      |                                  ^

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h: In member function ‘virtual bool URMessagePacketConsumer::consume(int)’:

/home/gert/ur_modern_driver/libur_modern_driver/../include/ur_modern_driver/ur/consumer.h:64:12: error: ‘packet’ was not declared in this scope; did you mean ‘RTPacket’?

   64 |     return packet->consumeWith(*this);

      |            ^~~~~~

      |            RTPacket

make[2]: *** [CMakeFiles/ur_driver_lib.dir/build.make:104: CMakeFiles/ur_driver_lib.dir/src/master_board.cpp.o] Error 1

make[1]: *** [CMakeFiles/Makefile2:83: CMakeFiles/ur_driver_lib.dir/all] Error 2

make: *** [Makefile:136: all] Error 2

