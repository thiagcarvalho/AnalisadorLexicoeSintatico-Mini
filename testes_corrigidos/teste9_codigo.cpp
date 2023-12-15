#include<iostream>
int main(){
float nota1, nota2, media;
std::cin>>(nota1);
std::cin>>(nota2);
media=(nota1+nota2)/2;
if((media>=6)){
std::cout<<("Aprovado!");
}
else{
std::cout<<("Reprovado.");
}
}