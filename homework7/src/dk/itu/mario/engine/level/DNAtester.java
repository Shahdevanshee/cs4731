package dk.itu.mario.engine.level;

import java.util.Random;
import java.util.*;
import dk.itu.mario.engine.level.MyDNA;

public class DNAtester {

    public static void main(String[] args) {
        MyDNA d1 = new MyDNA();
        // System.out.println(d1.getChromosome());
        // System.out.println(d1.getFitness());
        // System.out.println(d1.getLength());

        MyDNA d2 = new MyDNA();
        // System.out.println(d2.getChromosome());
        // System.out.println(d2.getFitness());
        // System.out.println(d2.getLength());

        MyDNA d3 = new MyDNA();

        d1.setChromosome("abcde");
        d3 = d1.mutate();
        System.out.println("d1: " + d1.getChromosome());
        System.out.println("d3: " + d3.getChromosome());
        d1.setChromosome("vwxyz");
        d3.setChromosome("abcde");
        System.out.println("d1: " + d1.getChromosome());
        System.out.println("d3: " + d3.getChromosome());
        ArrayList<MyDNA> list = d1.crossover(d3);
        System.out.println("d1: " + d1.getChromosome());
        System.out.println("d3: " + d3.getChromosome());
        System.out.println("list: " + list);
    }
}