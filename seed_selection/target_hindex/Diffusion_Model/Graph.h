#include<cstdlib>
#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
#include<list>
#include<map>
#include<set>
#include<iterator>
using namespace std;

class User;
class Edge;
class Graph;

class Edge{
	public:
		Edge(User* a, User* b, double v){
			u1 = a;
			u2 = b;
            w = v;
            
		}
		
		User* u1;
		User* u2;
        double w;		
};

class User{
	public:
		User(string s){
			id = s;
            is_seed = false;
            active = false;
            is_male = true;
		}		
        
        User(string s, bool m){
			id = s;
            is_seed = false;
            active = false;
            is_male = m;
		}

		string id;
		list<Edge*> friends;
        bool is_seed;
        bool active;
        bool is_male;
		
		void print(){
			cout << id << ": ";
            if(is_seed){
              cout << "seed ";
            }
            if(active){
              cout << "active";
            }
            cout <<endl;
		}

};

class Graph{
	public:
		Graph(){
		}
		
		list<User*> users;
        list<User*> seeds;
				
		User* get_user(string s, map<string, User*> &user_mapping){
		    if(user_mapping.find(s) != user_mapping.end()){
				return user_mapping[s];
			}
			return NULL;
		}				
        
        User* add_user(string s, string g, map<string, User*> &user_mapping){
			if(user_mapping.find(s) != user_mapping.end()){
				return user_mapping[s];
			}
			else{
                User* u;
                if(g == "1"){
                    u = new User(s, true);
                }
                else{
                    u = new User(s, false);
                }				
				user_mapping[s] = u;
				users.push_back(u);
				return u;
			}
		}
        
        User* add_user(string s, map<string, User*> &user_mapping){
			return add_user(s, "1", user_mapping);
		}
					
		Edge* add_edge(string a, string ga, string b, string gb, double w, map<string, User*> &user_mapping){
      		User* u1 = add_user(a, ga, user_mapping);
			User* u2 = add_user(b, gb, user_mapping);
			Edge* e = new Edge(u1, u2, w);
			u1->friends.push_back(e);
			return e;
		}
        
        Edge* add_edge(string a, string b, double w, map<string, User*> &user_mapping){
			return add_edge(a, "1", b, "1", w, user_mapping);
		}
        
        void add_seed(User* seed){
            seed->is_seed = true;
            seed->active = true;
            seeds.push_back(seed);
        }
        
        void unseeds(){
            for(list<User*>::iterator it = seeds.begin(); it != seeds.end(); it++){
                (*it)->is_seed = false;
                (*it)->active = false;
            }
            seeds.clear();
        }
        
        void reset(){
            for(list<User*>::iterator it = users.begin(); it != users.end(); it++){
                if(!(*it)->is_seed){
                    (*it)->active = false;
                }                 
            }
        }
						
		void print_users(){
			bool first = true;
			stringstream ss;
			for(list<User*>::iterator it = users.begin(); it != users.end(); it++){
				if(first){
					first = false;
				}
				else{
					ss << ", ";
				}
				ss << (*it)->id;
			}
			cout << ss.str() << endl;			
		}
};


Graph* read(string network, string seed_file, int k){
	Graph* g = new Graph();
	map<string, User*> user_mapping;
	
	// Read graph (whitespace separated file)
	cout << "Start reading graph" << endl;
	string filename = network;
	fstream f1;	
	f1.open(filename.c_str(), ios::in);
	if(!f1){
		cout << "Cannot open " << filename << endl;
	}
	else{
		char buffer[200];		
		while(!f1.eof()){
			f1.getline(buffer,sizeof(buffer));
            string s = "";
            list<string> token;
			if(buffer[0] == '\0'){
				break;
			}
			for(int i=0; buffer[i] != '\0' && buffer[i] != '\n' && buffer[i] != '\r'; i++){
				if(buffer[i] == ' '){
					token.push_back(s);
					s = "";
				}
				else{
				    s += buffer[i];
				}
			}
			token.push_back(s);
            list<string>::iterator it = token.begin();
            if(token.size() == 3){
                string id1 = *it;
                advance(it, 1);
                string id2 = *it;
                advance(it, 1);
                double value = std::stod(*it, NULL);
                g->add_edge(id1, id2, value, user_mapping);
            }		
			else if(token.size() == 5){
                string id1 = *it;
                advance(it, 1);
                string gender1 = *it;
                advance(it, 1);
                string id2 = *it;
                advance(it, 1);
                string gender2 = *it;
                advance(it, 1);
                double value = std::stod(*it, NULL);
                g->add_edge(id1, gender1, id2, gender2, value, user_mapping);
            }
		}
	}
    
    if(seed_file != ""){
        // Read seeds (a seed per line)
        cout << "Start reading seeds" << endl;
    	filename = seed_file;
    	fstream f2;	
    	f2.open(filename.c_str(), ios::in);
    	if(!f2){
    		cout << "Cannot open " << filename << endl;
    	}
    	else{
    		char buffer[200];		
    		while(!f2.eof()){
    			f2.getline(buffer,sizeof(buffer));
                string s = "";  
                if(buffer[0] == '\0'){
    				break;
    			}		
    			for(int i=0; buffer[i] != '\0' && buffer[i] != '\n' && buffer[i] != '\r'; i++){
    				s += buffer[i];
    			}
    			string id = s;	
    			User* seed = g->get_user(id, user_mapping);
                if(seed == NULL){
                    continue;
                }            
                g->add_seed(seed);
                if(k > 0 && g->seeds.size() == k){
                    break;
                } 
    	   }
    	}
    }    
    
	
	return g;
}

Graph* read(string network){
	return read(network, "", -1);
}

