package DE;



public class TRastrigin implements IFunction{
    private double fOpt;
    private int fDimension;

    public TRastrigin(int dimension, double opt) {
        fDimension = dimension;
        fOpt = opt;
    }

    public double evaluate(TVector vec) {
        double eval = 0.0;
        double cos = 0.0;
        for (int i = 0;i<fDimension;i++) {
            eval += (vec.getArray()[i] - fOpt) * (vec.getArray()[i] - fOpt);
            cos += 1.0 - Math.cos(2.0*Math.PI * (vec.getArray()[i] - fOpt));
        }
        return eval + 10.0 * cos;
    }
}
