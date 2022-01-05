#include <iostream>
#include <fstream>
#include <sstream>


using namespace std;

void parse_file(const string &filename, bool binary) {
    ifstream file(filename);

    if (!file.is_open()) {
        cerr << "Failed to open file '" << filename << "'!" << endl;
        exit(EXIT_FAILURE);
    }

    string line;
    uint16_t movie_id = -1;
    while (getline(file, line)) {
        if (line[line.length() - 1] == ':') {
            movie_id = stol(line.substr(0, line.length() - 1));
        } else {
            std::istringstream s(line);
            std::string customer_id_s, rating_s;
            getline(s, customer_id_s, ',');
            getline(s, rating_s, ',');

            if (binary) {
                // the byteorder is important, we convert from host to network (big endian)
                uint16_t movie_id_be = htons(movie_id);
                uint32_t customer_id = htonl(stoi(customer_id_s));
                uint8_t rating = stoi(rating_s);

                fwrite(&movie_id_be, sizeof(uint16_t), 1, stdout);
                fwrite(&customer_id, sizeof(uint32_t), 1, stdout);
                fwrite(&rating, sizeof(uint8_t), 1, stdout);
            } else {
                cout << movie_id << ',' << customer_id_s << ',' << rating_s << endl;
            }
        }
    }
}

#define BINARY

int main(int argc, const char *argv[]) {
    if (argc <= 1) {
        cerr << "No input files provided" << endl;
        exit(EXIT_FAILURE);
    }

    for (int i = 1; i < argc; i++) {
#ifdef BINARY
        parse_file(argv[i], true);
#else
        parse_file(argv[1], false);
#endif
    }

    return EXIT_SUCCESS;
}
