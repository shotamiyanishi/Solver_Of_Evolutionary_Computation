package DE;



public class TSphere implements IFunction{
    private double fOpt;
    private int fDimension;

    public TSphere(int dimension, double opt) {
        fDimension = dimension;
        fOpt = opt;
    }

    public double evaluate(TVector vec) {
        double eval = 0.0;
        for (int i = 0; i < fDimension; i++) {
            eval += (vec.getArray()[i] - fOpt) * (vec.getArray()[i] - fOpt); 
        }
        return eval;
    }
}
