#include<iostream>
int main(){
int a, b, c, maior;
std::cin>>(a);
std::cin>>(b);
std::cin>>(c);
if(((a>b)&&(a>c))){
maior=a;
}else{
if((b>c)){
maior=b;
}
else{
maior=c;
}
}
std::cout<<(maior);
}