function accuracy = lambda_accuracy(X, y, folds, lambda)
	indices = crossvalind('Kfold',X(:,1),folds);
	accuracy = 0;

	for j=1:folds
		% Get train/test folds
		test = (indices == j);
		train = xor(1,test);

		Xtrain = X(train, :);
		ytrain = y(train, :);

		Xtest = X(test, :);
		ytest = y(test, :);

		% Initialize fitting parameters
		initial_theta = zeros(size(X, 2), 1);

		% Options
		options = optimset('GradObj', 'on', 'MaxIter', 400);

		% Optimize
		[theta, ~, ~] = ...
			fminunc(@(t)(cost_func_reg(t, Xtrain, ytrain, lambda)), initial_theta, options);

		% Compute accuracy on our training set
		p = predict(theta, Xtest);

		% Accuracy
		accuracy = accuracy + (mean(double(p == ytest)) * 100);
	end

	accuracy = accuracy / folds;
end