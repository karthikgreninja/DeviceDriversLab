#!/bin/sh

echo "Basic Shell Scripting"
echo "Presented by Karthikeyan S"

echo "For Loop"
echo "Enter the maximum value till which values need to be displayed"
read number
echo "Output is as Follows"
for ((i=1;i<=number;i++))
do
 echo "$i"
done
echo

echo "Sorting Algorithm"
echo "Enter total number of elements"
read n
echo "Enter Numbers in the array:"
for (( i = 0; i < $n; i++ ))
do
read nos[$i]
done
echo "Numbers in the array are:"
for (( i = 0; i < $n; i++ ))
do
echo ${nos[$i]}
done
for (( i = 0; i < $n ; i++ ))
do
for (( j = $i; j < $n; j++ ))
do
if [ ${nos[$i]} -gt ${nos[$j]}  ]; 
then
t=${nos[$i]}
nos[$i]=${nos[$j]}
nos[$j]=$t
fi
done
done
echo -e "Sorted Numbers are as follows "
for (( i=0; i < $n; i++ ))
do
echo ${nos[$i]}
done
echo

echo "Linea Search"
echo “Enter the total number of elements:”
read no
echo “Enter the numbers”
for(( i=0 ;i<no; i++ ))
do
read m
a[i]=$m
done
for(( i=1; i<no; i++ ))
do
for(( j=0; j<no-i; j++))
do
if [ ${a[$j]} -gt ${a[$j+1]} ]
then
t=${a[$j]}
a[$j]=${a[$j+1]}
a[$j+1]=$t
fi
done
done
echo “Sorted array is”
for(( i=0; i<no; i++ ))
do
echo “${a[$i]}”
done
echo “Enter the element to be searched :”
read s
l=0
c=0
u=$(($no-1))
while [ $l -le $u ]
do
mid=$(((( $l+$u ))/2 ))
if [ $s -eq ${a[$mid]} ]
then
c=1
break
elif [ $s -lt ${a[$mid]} ]
then
u=$(($mid-1))
else
l=$(($mid+1))
fi
done
if [ $c -eq 1 ]
then
echo “Element found at position $(($mid+1))”
else
echo “Element not found”
fi
echo

echo "Chatbot"
INPUT_STRING=Hello
echo $INPUT_STRING
while [ "$INPUT_STRING" != "quit" ]
do
  echo "Please type something in (quit to quit)"
  read INPUT_STRING
  echo "You typed: $INPUT_STRING"
done
echo

echo "Swtch Case"
echo "Test Message. Hello ?"
echo "Possible Answers - hello, quit"
while :
do
  read INPUT_STRING
  case $INPUT_STRING in
	hello)
		echo "Hello yourself!"
		;;
	bye)
		echo "See you again!"
		break
		;;
	*)
		echo "Sorry, I don't understand"
		;;
  esac
done
echo 


echo "Prime number App"
#storing the number to be checked 
echo -n "Enter a number: "
read number
i=2 
  
#flag variable 
f=0 
  
#running a loop from 2 to number/2 
while test $i -le `expr $number / 2`  
do
  
#checking if i is factor of number 
if test `expr $number % $i` -eq 0  
then
f=1 
fi
  
#increment the loop variable 
i=`expr $i + 1` 
done
if test $f -eq 1  
then
echo "Not Prime"
else
echo "Prime"
fi

echo "Factorial App"
echo -n "Enter a number: "
read num
factorial=1
for(( i=1; i<=num; i++ ))
do
  factorial=$[ $factorial * $i ]
done
echo "The factorial of $number is $factorial"
echo

echo "Calculator App"
echo "Enter Two numbers : "
read a 
read b 
echo "Enter Choice :"
echo "1. Addition"
echo "2. Subtraction"
echo "3. Multiplication"
echo "4. Division"
read ch 
case $ch in
  1)res=`echo $a + $b | bc` 
  ;; 
  2)res=`echo $a - $b | bc` 
  ;; 
  3)res=`echo $a \* $b | bc` 
  ;; 
  4)res=`echo "scale=2; $a / $b" | bc` 
  ;; 
esac
echo "Result : $res"
echo

echo "Function"
print() 
{
echo Pokemon $1
}
print Greninja
print Pikachu
print Charizard
print Infernape
echo







