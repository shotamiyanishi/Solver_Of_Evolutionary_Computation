package DE;



import java.util.Random;

public class TDEMain {
    
    public static void main(String[] args) {
        int dimension = 10;
        int populationSize = 80;
        double max = 5.0;
        double min = -5.0;
        double opt = 2.0;
        long seed = 0L;
        Random rand = new Random(seed);
        TDE de = new TDE(dimension, populationSize, max, min, rand);
        IFunction function = new TSphere(dimension, opt);
        int maxIteration = 100;
        de.initialize(function);
        for (int gen = 0; gen < maxIteration; gen++) {
            de.doOneGeneration(function);
        }
    }
}
