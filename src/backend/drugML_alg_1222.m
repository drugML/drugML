dim = size(X_train);
num_col = dim(2); 
num_row = dim(1); % get the number of column and row in the data


%% closest average
pos_inst = find(X_train(:,num_col) == 1); % row indices of drugs that are valid
neg_inst = find(X_train(:,num_col) == 0); % ...invalid
pos_avg = mean(X_train(pos_inst,2:num_col-1)); % an average vector of all valid drugs
neg_avg = mean(X_train(neg_inst,2:num_col-1)); % ...invliad drugs
% excluding the first and last column, which are indices and labels


class_label = zeros(9,0);
for i = 1:num_row
    curr_avg = mean(X_train(i,2:num_col-1));
    curr_diff_pos = abs(curr_avg-pos_avg);
    curr_diff_neg = abs(curr_avg-neg_avg);
    
    if curr_diff_pos > curr_diff_neg
        class_label(i) = 1;
    else
        class_label(i) = 0;
    end
end

acc = sum(class_label)/sum(X_train(:,num_col));

%% naive bayes

% part1: discretization based on information gain
num_valid = sum(X_train(:,num_col)== 1);
num_invalid = sum(X_train(:,num_col)== 0); % number of valid and invalid drugs

frac_valid = num_valid/num_row;
frac_invalid = 1-frac_valid; % calculate the fraction
orig_entropy = -(frac_valid * log2(frac_valid) + frac_invalid * log2(frac_invalid));
% then original entropy

best_threshold_per_feature = [];
for i=2:num_col-1
    IG_per_threshold = [];
    for j=1:num_row
        curr_col = X_train(:,i);
        curr_threshold = X_train(j,i);
       
        smaller_idx = find(curr_col<curr_threshold); 
        larger_idx = find(curr_col>curr_threshold); % split into two classes
        % based on the threshold
        
        smaller_valid = sum(X_train(smaller_idx,num_col)==1); 
        % # of valid drugs that are smaller than threshold
        smaller_inv = sum(X_train(smaller_idx,num_col)==0);
        
        larger_valid = sum(X_train(larger_idx,num_col)==1); 
        % # of valid drugs that are smaller than threshold
        larger_inv = sum(X_train(larger_idx,num_col)==0);
        
        % calculate the fraction of label1 and 0 for each group greater or
        % smaller than threshold
        % add 0.00001 to avoid log(0) = -inf
        smaller_frac_valid= smaller_valid/length(smaller_idx);
        larger_frac_valid = larger_valid/length(larger_idx);
        
        % now calculate entropy for each group smaller or larger than
        % treshold
        class_smaller_entropy = -(smaller_frac_valid * log2(smaller_frac_valid) + (1-smaller_frac_valid) * log(1-smaller_frac_valid+0.00001));
        class_larger_entropy = -(larger_frac_valid * log2(larger_frac_valid) + (1-larger_frac_valid) * log(1-larger_frac_valid+0.00001));

        IG = orig_entropy - length(smaller_idx)/num_row*class_smaller_entropy - length(larger_idx)/num_row*class_larger_entropy;
        IG_per_threshold = [IG_per_threshold, IG];
    end
    [M,I] = min(IG_per_threshold);
    best_thres = X_train(I,i);
    best_threshold_per_feature = [best_threshold_per_feature,best_thres];
end 

% now discretize the data based on the best threshold
bin_data = zeros(num_row,num_col);
bin_data(:,1) = X_train(:,1);
bin_data(:,num_col) = X_train(:,num_col);
for c = 2:num_col-1
    for r = 1:num_row
        if X_train(r,c) > best_threshold_per_feature(c-1)
            bin_data(r,c) = 1;
        else 
            bin_data(r,c) = 0;
        end
    end
end 
        
% part2: discretization based on ....
% now discretize the data based on the best threshold

% part3: 






