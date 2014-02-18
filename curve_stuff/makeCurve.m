x = [0:0.1:15];
firstX = [0:0.1:1.5];
secondX = [1.6:0.1:15];
y1 = cos(pi*firstX/6);
y2 = 2.^(-secondX/3);
y = [y1 y2];
plot(x,y)
