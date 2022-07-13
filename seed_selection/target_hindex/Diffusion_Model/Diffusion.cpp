#include<cstdlib>
#include<iostream>
#include<random>
#include<string>
#include<sstream>
#include<utility>
#include<fstream>
#include "Graph.h"

using namespace std;

int main(int argc, char* argv[]){
	// network, seed_file, k, rho, sampling
	string network = "network";
    string seed_file = "seeds";
    int k = -1;
    double rho = 1.0;
	int sampling = 1000;
	
	if(argc >= 4){
		network = argv[1];
        seed_file = argv[2];
        k = std::stoi(argv[3], NULL);
        if(argc >= 5){
            rho = std::stod(argv[4], NULL);
            if(argc >= 6){
                sampling = std::stoi(argv[5], NULL);
            }
        }          		
	}
 
	
	Graph* g = read(network, seed_file, k);
	// cout << "Finish reading" << endl;
	
    std::random_device rd;
    std::default_random_engine gen = std::default_random_engine(rd());
    std::uniform_real_distribution<> dis(0, 1);
  
	double spread_m = 0.0;
    double spread_f = 0.0;
    for(int i=0; i<sampling; i++){
        // cout << i << endl;
        list<User*> current;
        for(list<User*>::iterator it = g->seeds.begin(); it != g->seeds.end(); it++){
            if((*it)->is_male){
                spread_m += 1;
            }
            else{
                spread_f += 1;
            }
            current.push_back(*it);
        }
        
        while(current.size() > 0){
            list<User*> next;
            for(list<User*>::iterator it = current.begin(); it != current.end(); it++){
                User* u = *it;
                for(list<Edge*>::iterator fit = u->friends.begin(); fit != u->friends.end(); fit++){
                    User* v = (*fit)->u2;
                    double w = (*fit)->w;
                    if(!v->active && ((u->is_male == v->is_male) || dis(gen) < rho) && dis(gen) < w){
                        v->active = true;
                        if(v->is_male){
                            spread_m += 1;
                        }
                        else{
                            spread_f += 1;
                        }
                        next.push_back(v);
                    }
                }
            }
            current.clear();
            current = next;
            next.clear();
        }
        g->reset();        
    }
    spread_m /= (double)sampling;
    spread_f /= (double)sampling;
    		

	//cout<<spread_m<<endl;
        //cout<<spread_f<<endl;
	// output
	stringstream ss;
	ss<<network<<"_"<<seed_file.substr(15,-4)<<".out";
	//cout<<ss<<endl;
        fstream ff;
	ff.open(ss.str(), ios::out);
	//cout<<spread_m<<endl;
        //cout<<spread_f<<endl;
	ff << spread_m << "\t" << spread_f << endl;
	ff.close();
        //cout<<"hi"<<endl;

	//Create and open a text file
	//ofstream MyFile("filename.txt");
	
	   
	//MyFile << "Files can be tricky, but it is fun enough!";
	
	        // Close the file
	//MyFile.close();


}
