function g = sigmoid(z)
	g = 1 ./ (exp(-z) + 1);
end
