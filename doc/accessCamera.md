# Documentatie voor hoe te verbinden met de camera op de Unitree Go 1

Try 3 lijkt te werken bij Bart, dus ik basseer me op dit stuk doc

## Change yaml and recompile

Aan te passen om de nano:

* ip address naar .162
* indentificeer device
* indentificeer protocol

Zie aangepaste yaml file in de folder accessCamera onder de root.

Daarna sommigen processen killen.

De processen checken welke aan het runnen zijn:
```
$ ps -aux | grep point_cloud_node
$ ps -aux | grep mqttControlNode
$ ps -aux | grep live_human_pose
```

Te killen door:
```
ps -aux | grep point_cloud_node | awk '{print $2}' | xargs kill -9
ps -aux | grep mqttControlNode | awk '{print $2}' | xargs kill -9
ps -aux | grep live_human_pose | awk '{print $2}' | xargs kill -9
```

Kleine aanpassing aan de get image trans example, ook in de accessCamera folder.

Als je daarna dit commando runt, dan zou je frames van de camera moeten zien:
```
$ ./bins/example_getimagetrans 
```