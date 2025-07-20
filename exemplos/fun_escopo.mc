int fun() {
    int x = 10;
    int y = 5;
    while (x < 11) {
        x = x + 1;
    }
    return x + y; 
}

int main() {
    return fun();
}