# connecteren met de bot

NAT veranderen door Bridged, name veranderen van wifi naar de ethernet en promiscous modus -> alles toestaan

eigen ip veranderen:

```
sudo ip a add 192.168.123.162/24 dev enp46s0
```

daarna verbinden met de bot:

```
ssh unitree@192.168.123.13
```

password: 123

processen killen:
```
kill -9 pip code
```

ps -aux | grep point_cloud_node | awk '{print $2}' | xargs kill -9

ps -aux | grep mqttControlNode | awk '{print $2}' | xargs kill -9

ps -aux | grep | awk '{print $2}' | xargs kill -9

ps -aux | grep point_cloud_node | awk '{print $2}' | xargs kill -9

ps -aux | grep camerarosnode | awk '{print $2}' | xargs kill -9

ps -aux | grep mqtt | awk '{print $2}' | xargs kill -9

~                                                      

