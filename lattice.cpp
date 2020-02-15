include <iostream>
#include <vector>
#include <cstdlib>
#include <cstdio>
#include <random>
#include <fstream>
#include <ctime>

using namespace std;

/*
  <random> is recommended in C++ over using rand because rand is seeded with
  time, but this is updated only every second. So if we were to for some
  reason run the file several times within the same second, we would get
  the exact same results.

  <random> is also recommended over rand() since:

  rand() is typically a low quality pRNG and not suitable for applications 
  that need a reasonable level of unpredictability. <random> provides a 
  variety of engines with different characteristics suitable for many 
  different use cases.
  
  We say rand() is aa poor quality pRNG because if we generate a sequence of
  numbers and then group them in 2's and plot as coordinates, we will see patterns.

  Converting the results of rand() into a number you can use directly usually 
  relies on code that is difficult to read and easy to get wrong, whereas 
  using <random> distributions is easy and produces readable code.

  The common methods of generating values in a given distribution using 
  rand() further decrease the quality of the generated data. % generally biases 
  the data and floating point division still produces non-uniform distributions. 
  <random> distributions are higher quality as well as more readable.

  rand() relies on a hidden global resource. Among other issues this causes 
  rand() to not be thread safe. Some implementations make thread safety guarantees,
  but this is not required standard. Engines provided by <random> encapsulate 
  pRNG state as objects with value semantics, allowing flexible control over the state.

  srand() only permits a limited range of seeds. Engines in <random> can be initialized 
  using seed sequences which permit the maximum possible seed data. seed_seq also 
  implements a common pRNG warm-up.
  
  from StackOverflow answer: 
  https://stackoverflow.com/questions/18726102/what-difference-between-rand-and-random-functions
  https://channel9.msdn.com/Events/GoingNative/2013/rand-Considered-Harmful
*/

// set up random generator and define seed for each
random_device rd;
mt19937 generator(rd());

class Lattice {
public:
	// variables
	int dimensions;
	vector<int> coordinates;

	// constructor
	Lattice(int d){
		dimensions = d;

		// fills coordinate array with zeros
		// can probably be done with coordinates.assign(...)
		for(int i=0; i<d; i++){
			coordinates.push_back(0);
		}
	}

	// move function
	void move(){
		// int direction = rand()%dimensions;
		// int distance = rand()%2;

		uniform_int_distribution<> distribution1(0,dimensions-1);
		int direction = distribution1(generator);

		uniform_int_distribution<> distribution2(0,1);
		int distance = distribution2(generator);

		// so that distance is always -1 or 1
		if(distance == 0){
			distance = -1;
		}
		coordinates[direction] = coordinates[direction] + distance;
	}

	// caught function
	bool caught(double probability){
		uniform_real_distribution<double> distribution3(0.0,1.0);
		double number = distribution3(generator);

		if(number < probability){
			return true;
		}
		return false;
	}

};

int main(int argc, char* argv[]){
	// to do, take command line arguments to decide number of iterations and probability
	// make python function feed these arguments

	// probably unnecessary
	srand(time(NULL));   

	int dimen = atoi(argv[1]);
	double probability = atof(argv[2]);
	int iterations = atoi(argv[3]);

	// cout << dimen << endl;
	// cout << probability << endl;
	// cout << iterations << endl;

	// int dimen = 8;
	Lattice lattice(dimen);
    
	vector<int> data;

	// run the random walk
	for(int i=0; i<iterations; i++){
		bool caught = false;
		int time = 0;
		while(caught != true){
			time++;
			lattice.move();
			caught = lattice.caught(probability);
		}
		// append to data
		data.push_back(time);
	}

	ofstream myfile;
	myfile.open("data.dat");
	for(int i=0; i<data.size(); i++){
		myfile << data[i] << "\n";
	}
	myfile.close();
	return 0;
}
