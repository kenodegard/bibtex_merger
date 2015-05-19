function [J, grad] = cost_func_reg(theta, X, y, lambda)
	m = length(y); % number of training examples

	J = (-1 * transpose(y) * log(sigmoid(X * theta)) - ...
		(transpose(1 - y) * log(1 - sigmoid(X * theta)))) / m + ...
		((lambda / (2 * m)) * sum(theta(2:end) .^ 2));

	grad = ((transpose(X) * ((sigmoid(X * theta)) - y)) ./ m) + ...
		([0; theta(2:end)] .* (lambda / (2 * m)));
end