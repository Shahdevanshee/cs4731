package dk.itu.mario.engine.level;

import java.util.Random;
import java.util.*;

//Make any new member variables and functions you deem necessary.
//Make new constructors if necessary
//You must implement mutate() and crossover()


public class MyDNA extends DNA
{

    public int numGenes = 0; //number of genes

    // Return a new DNA that differs from this one in a small way.
    // Do not change this DNA by side effect; copy it, change the copy, and return the copy.
    public MyDNA mutate ()
    {
        MyDNA copy = new MyDNA();
        //YOUR CODE GOES BELOW HERE
        String alpha = "abcdefghijklmnopqrstuvwxyz";
        Random r = new Random();
        int loc = r.nextInt(this.getChromosome().length());
        int letter = r.nextInt(alpha.length());
        String ret = "";
        for (int i = 0; i < this.getChromosome().length(); i++) {
            if (i == loc) {
                ret += alpha.charAt(letter);
            } else {
                ret += this.getChromosome().charAt(i);
            }
        }
        copy.setChromosome(ret);
        //YOUR CODE GOES ABOVE HERE
        return copy;
    }

    // Do not change this DNA by side effect
    public ArrayList<MyDNA> crossover (MyDNA mate)
    {
        ArrayList<MyDNA> offspring = new ArrayList<MyDNA>();
        //YOUR CODE GOES BELOW HERE
        // TODO might want this to be random
        Random r = new Random();
        int middle = (int)(r.nextInt(this.getChromosome().length()));
        MyDNA child1 = new MyDNA();
        MyDNA child2 = new MyDNA();

        String one = this.getChromosome().substring(0, middle) + mate.getChromosome().substring(middle, mate.getChromosome().length());
        String two = mate.getChromosome().substring(0, middle) + this.getChromosome().substring(middle, this.getChromosome().length());

        child1.setChromosome(one);
        child2.setChromosome(two);
        offspring.add(child1);
        offspring.add(child2);
        //YOUR CODE GOES ABOVE HERE
        return offspring;
    }

    // Optional, modify this function if you use a means of calculating fitness other than using the fitness member variable.
    // Return 0 if this object has the same fitness as other.
    // Return -1 if this object has lower fitness than other.
    // Return +1 if this objet has greater fitness than other.
    public int compareTo(MyDNA other)
    {
        int result = super.compareTo(other);
        //YOUR CODE GOES BELOW HERE

        //YOUR CODE GOES ABOVE HERE
        return result;
    }


    // For debugging purposes (optional)
    public String toString ()
    {
        String s = super.toString();
        //YOUR CODE GOES BELOW HERE

        //YOUR CODE GOES ABOVE HERE
        return s;
    }

    public void setNumGenes (int n)
    {
        this.numGenes = n;
    }

}

