#include <iostream>
using namespace std;

class Dumpling{
public:
	virtual ~Dumpling(){};
	virtual void showDressing()=0;
};

class MeatDumpling:public Dumpling{
public:
	void showDressing(){
		cout<< "Add meat"<<endl;
	}
	~MeatDumpling(){cout<< "~MeatDumpling()"<<endl;};
};

class DecoratorDumpling:public Dumpling{
public:
	DecoratorDumpling(Dumpling *d):m_d(d){}
	void showDressing(){
		m_d->showDressing();
	}
	~DecoratorDumpling(){cout<< "~DecoratorDumpling()"<<endl;};
private:
	Dumpling *m_d;
};

class SaltDumpling:public DecoratorDumpling{
public:
	SaltDumpling(Dumpling* d):DecoratorDumpling(d){};
	void showDressing(){
		DecoratorDumpling::showDressing();
		cout << "Add salt"<<endl;
	}
	~SaltDumpling(){cout<< "~SaltDumpling()"<<endl;};
};

class OilDumpling:public DecoratorDumpling{
public:
	OilDumpling(Dumpling* d):DecoratorDumpling(d){};
	void showDressing(){
		DecoratorDumpling::showDressing();
		cout << "Add oil"<<endl;
	}
	~OilDumpling(){cout<< "~OilDumpling()"<<endl;};
};


int main(){
	Dumpling *d = new MeatDumpling();
	Dumpling *d1 = new SaltDumpling(d);
	Dumpling *d2 = new OilDumpling(d1);
	d2->showDressing();
	delete d;
	delete d1;
	delete d2;
	return 0;
}
