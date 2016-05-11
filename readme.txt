Read Me
Machine Learning
Authors: Robert Parrillo, Juan David Dominguez, Michael Gofron

Recommended: Use pypy as the algorithm takes a while for large data sets (20 mins + with pypy)


To run use python treeCom.py with command line inputs.

Command line inputs:
	nt Datafile NewTreeName
		Creates a new tree model where Datafile is the "".csv file that is formatted similar to that of the hw. NewTreeName is the name of the tree that is created. If specified with other commands, it will use the new tree created for the other commands.

		Ex/ python treeCom.py nt btrain.csv btrainTree
			Creates a tree named "btrainTree"
	rt TreeName
		Command line that specifies to re-use a tree that has already been created by the command line nt. CANNOT be used with nt. Is supposed to be used with other command lines (tc, p, np, etc) to use a model that has already been saved--without need to create a again.

		Ex/ python treeCom.py rt btrainTree nv bvalidate.csv bvalidateData p
			Will use the tree named "btrainTree" with the commands nv and p.
	nv ValidationFile ValidationName
		Will create a new validation object from a "".csv file. The first imput is the name of the file. The second input is the name of the validation object. Used with other command line arguments, it will use that validation object to work on the rest of the arguments.

		Ex/ python treeCom.py nv bvalidate.csv bvalidateData
			Will create the validation object named bvalidateData from the bvalidate.csv

	rv ValidationName
		Will reuse a validation object--one that has been saved-- for the other commands.

		Ex/ python treeCom.py rt treeName rv bvalidateData p
			Will use the validation object named bvalidateData with command rt (reusing a tree) for the command p

	tc classifiedFileIn classifiedFileOut
		Command line that creates a .csv file guessing the final classfication. The input afterwards specifies the name of the file that will be classified. The second input is the file name that you want to create.

		Must be used with nt or rt!

		Ex/ python treeCom.py nt btrain.csv btrainTree tc btest.csv btestNew.csv
			This will create the tree from btrain.csv, name it btrainTree; then, it will use the tree btrainTree to classify 

		Ex/ python treeCom.py rt btrainTree tc btest.csv btestNew.csv
			This will reuse the tree btrainTree to create the file btestNew that guesses the classifications of btest.
	p
		Command line that prints a Disjunctive Normal Form of a tree before and after being pruned. Furthermore, it prints the percentage correct before and after pruning with a validation set.

		Must be used with (nt or rt) and (nv or rv)!

		Ex/ python treeCom.py rt btrainTree rv bvalidateData p
	np
		Command line that prints a Disjunctive Normal Form of a tree without pruning. Furthermore, it prints the percentage correct without pruning with a validation set.

		Must be used with (nt or rt) and (nv or rv)!

		Ex/ python treeCom.py rt btrainTree rv bvalidateData np