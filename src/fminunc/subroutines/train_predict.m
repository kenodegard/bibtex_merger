function [theta, predictTrain, accuracyTrain, predictTest] = train_predict(Xtrain, ytrain, Xtest, lambda)
	% Generate theta for lambda
	initial_theta = zeros(size(Xtrain,2),1);
	options = optimset('GradObj', 'on', 'MaxIter', 400);
	[theta, ~, ~] = ...
		fminunc(@(t)(cost_func_reg(t, Xtrain, ytrain, lambda)), initial_theta, options);

	% Compute accuracy on test set
	predictTrain = predict(theta, Xtrain);
	accuracyTrain = mean(double(predictTrain == ytrain)) * 100;

	% Compute accuracy on test set
	predictTest = predict(theta, Xtest);
end