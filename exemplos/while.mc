int main() {
    int x = 0;
    int y = 2;
    while (x < 1) {
        int y = 5;
        x = x + 1;
    }
    return x + y; 
}