function [best_lambda, best_accuracy] = find_best_lambda(X, y, lambdas, folds)
	% Only loop and search for best lambda if more than one is given
	if length(lambdas) > 1
		accuracies = zeros(length(lambdas), 2);
		
		parfor i = 1:length(lambdas)
            lambda = lambdas(i)
            fprintf('starting testing for lambda = %3.2f', lambda);
			accuracies(i, :) = [lambda, lambda_accuracy(X, y, folds, lambda)];
		end

		plot(accuracies(:,1), accuracies(:,2));
		hold on;
		title('\lambda vs. Accuracy');
		xlabel('\lambda');
		ylabel('Accuracy (%)');
		axis([min(lambdas), max(lambdas), 0, 100]);
		hold off;

		best = accuracies(accuracies(:,2) == max(accuracies(:,2)), :);
		best_lambda = best(1,1);
		best_accuracy = best(1,2);
	else
		best_lambda = lambdas(1)
		best_accuracy = lambdaCrossval(X, y, folds, best_lambda);
	end
end