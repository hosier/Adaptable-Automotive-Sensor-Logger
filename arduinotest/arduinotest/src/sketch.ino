struct sensorData
{
	char beginPad[5];
	int data0;
	char pad0;
	//int data1;
	//char pad1;
	//int data2;
};

union data
{
	unsigned char buffer[sizeof(sensorData)];
	sensorData vars;
};

data sendData;

void setup()
{
	Serial.begin(9600);
	
	static char temp[5] = {0, 1, 2, 3, 4};
	memcpy(sendData.vars.beginPad, temp, 5);
	sendData.vars.pad0 = 0;
	//sendData.vars.pad1 = 0;
}

void loop()
{
	sendData.vars.data0 = (256);
	//sendData.vars.data1 = (512);
	//sendData.vars.data2 = (1024);
	//Serial.write(sendData.buffer, sizeof(sensorData));
	for (char i = 0; i < 100; ++i) {
		Serial.write(i);
		delay(100);
	}
	for (char i = 100; i >= 0; --i) {
		Serial.write(i);
		delay(10);
	}
	//delay(100);
}
