#include<iostream>
int main(){
int a, b, c, maior;
std::cin>>(a);
std::cin>>(b);
std::cin>>(c);
maior=((a>b)&&(a>c))?a:((b>c))?b:c;
std::cout<<(maior);
}