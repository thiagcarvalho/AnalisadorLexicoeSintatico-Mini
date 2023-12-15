#include<iostream>
int main(){
int id, qtd, cont, soma;
qtd=5;
cont=5;
soma=0;
do{
std::cout<<("Idade: ");
std::cin>>(id);
soma=soma+id;
cont=cont-1;
}while((cont>0));
std::cout<<("Media: ");
std::cout<<(soma/qtd);
}