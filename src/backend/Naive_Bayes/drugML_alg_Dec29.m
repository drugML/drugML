dim = size(X_train);
num_col = dim(2); 
num_row = dim(1); % get the number of column and row in the data

%%
%%%%%%%%%%%%%%%%%%%%% naive bayes %%%%%%%%%%%%%%%%%%%%%

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
bin_data_IG = zeros(num_row,num_col);
bin_data_IG(:,1) = X_train(:,1);
bin_data_IG(:,num_col) = X_train(:,num_col);
for c = 2:num_col-1
    for r = 1:num_row
        if X_train(r,c) > best_threshold_per_feature(c-1)
            bin_data_IG(r,c) = 1;
        else 
            bin_data_IG(r,c) = 0;
        end
    end
end 
        

%% part2: discretization based on k-means clustering
% cropped_X_train = X_train(:,2:num_col); % w/o index and class label
bin_data_cluster = zeros(num_row,num_col);
bin_data_cluster(:,1) = X_train(:,1);
bin_data_cluster(:,num_col) = X_train(:,num_col);

for column = 2:num_col-1
    clust = kmeans(cropped_X_train(:,column),2);
    clust(clust == 2) = 0; % replace all the cluster "2" to label "0"
    bin_data_cluster(:,column) = clust;
end
    
    % for every column, cluster that column into two classes, one
    % with label0 and one with label 1


%% part3-1: naive bayes calculation based on bin_data_IG

% shuffle the rows around to make sure discretization is randomized
bin_data_IG = bin_data_IG(randperm(size(bin_data_IG, 1)), :);

% P(y = 1)  and P(y = 0)
P_0_prior = sum(X_train(:,num_col)==0)/length(X_train(:,num_col));
P_1_prior = sum(X_train(:,num_col)==1)/length(X_train(:,num_col));

valid_set_idx = find(bin_data_IG(:,num_col)==1);
valid_set = bin_data_IG(valid_set_idx,:);
inv_set_idx = find(bin_data_IG(:,num_col)==0);
inv_set = bin_data_IG(inv_set_idx,:);

% conditional probability
condP = zeros(num_col-2,4); % to store conditional probability of each feature
% P(x1 = 1|y=1),P(x1 = 0|y=1), P(x1=1|y=0),P(x1=0|y=0)
% P(x2 = 1|y=1),P(x2 = 0|y=1), P(x2=1|y=0),P(x2=0|y=0)
% so on....
for feature = 2:num_col-1 % again, don't include index and class label
    
    condP_0_given_0 = sum(inv_set(:,feature) == 0)/length(inv_set); %P[(x=0)|(y=0)]
    condP_1_given_0 = sum(inv_set(:,feature) == 1)/length(inv_set); %P[(x=1)|(y=0)]
    
    condP_0_given_1 = sum(valid_set(:,feature) == 0)/length(valid_set); %P[(x=0)|(y=1)]
    condP_1_given_1 = sum(valid_set(:,feature) == 1)/length(valid_set); %P[(x=1)|(y=1)]
    condP(feature-1,:) = [condP_0_given_0, condP_1_given_0, condP_0_given_1, condP_1_given_1];
end

predP_per_drug = zeros(num_row,2); % store the numerical probability of predicting 1 and 0
predC_per_drug = []; % store the predicted label 
for drug = 1:num_row % for a particular drug
    pred_P_0 = P_0_prior; % probability of predicting y = 0 (start with prior probability for multiplication)
    pred_P_1 = P_1_prior; %  p....  y = 1
    
    for feature = 2:num_col-1 % for each feature of the drug
        curr_identity = bin_data_IG(drug,feature); % is the feature turned on, 0 or 1?
        if curr_identity == 0
            pred_P_0 = pred_P_0*condP(feature-1,1); % index into condP and find P(x=0|y=0)
            pred_P_1 = pred_P_1*condP(feature-1,3); %...P(x=0|y=1)
        else
            pred_P_0 = pred_P_0*condP(feature-1,2); %...P(x=1|y=0)
            pred_P_1 = pred_P_1*condP(feature-1,4); %...P(x=1|y=1)
        end
    end % iterate through every feature until all are multiplied
    
    predP_per_drug(drug,:) = [pred_P_0,pred_P_1];
    if pred_P_0 > pred_P_1
        predC_per_drug = [predC_per_drug,0];
    else
        predC_per_drug = [predC_per_drug,1];
    end
end

num_corr_pred = 0; % number of correctly predicted instances
for drug = 1:num_row
    if X_train(drug,num_col) == predC_per_drug(drug)
        num_corr_pred = num_corr_pred + 1;
    end
end

acc = num_corr_pred/num_row; % accuracy 
        
%% part3-2: naive bayes calculation based on bin_data_cluster

        
% shuffle the rows around to make sure discretization is randomized
bin_data_cluster = bin_data_cluster(randperm(size(bin_data_cluster, 1)), :);

% P(y = 1)  and P(y = 0)
P_0_prior = sum(X_train(:,num_col)==0)/length(X_train(:,num_col));
P_1_prior = sum(X_train(:,num_col)==1)/length(X_train(:,num_col));

valid_set_idx = find(bin_data_cluster(:,num_col)==1);
valid_set = bin_data_cluster(valid_set_idx,:);
inv_set_idx = find(bin_data_cluster(:,num_col)==0);
inv_set = bin_data_cluster(inv_set_idx,:);

% conditional probability
condP = zeros(num_col-2,4); % to store conditional probability of each feature
% P(x1 = 1|y=1),P(x1 = 0|y=1), P(x1=1|y=0),P(x1=0|y=0)
% P(x2 = 1|y=1),P(x2 = 0|y=1), P(x2=1|y=0),P(x2=0|y=0)
% so on....
for feature = 2:num_col-1 % again, don't include index and class label
    
    condP_0_given_0 = sum(inv_set(:,feature) == 0)/length(inv_set); %P[(x=0)|(y=0)]
    condP_1_given_0 = sum(inv_set(:,feature) == 1)/length(inv_set); %P[(x=1)|(y=0)]
    
    condP_0_given_1 = sum(valid_set(:,feature) == 0)/length(valid_set); %P[(x=0)|(y=1)]
    condP_1_given_1 = sum(valid_set(:,feature) == 1)/length(valid_set); %P[(x=1)|(y=1)]
    condP(feature-1,:) = [condP_0_given_0, condP_1_given_0, condP_0_given_1, condP_1_given_1];
end

predP_per_drug = zeros(num_row,2); % store the numerical probability of predicting 1 and 0
predC_per_drug = []; % store the predicted label 
for drug = 1:num_row % for a particular drug
    pred_P_0 = P_0_prior; % probability of predicting y = 0 (start with prior probability for multiplication)
    pred_P_1 = P_1_prior; %  p....  y = 1
    
    for feature = 2:num_col-1 % for each feature of the drug
        curr_identity = bin_data_cluster(drug,feature); % is the feature turned on, 0 or 1?
        if curr_identity == 0
            pred_P_0 = pred_P_0*condP(feature-1,1); % index into condP and find P(x=0|y=0)
            pred_P_1 = pred_P_1*condP(feature-1,3); %...P(x=0|y=1)
        else
            pred_P_0 = pred_P_0*condP(feature-1,2); %...P(x=1|y=0)
            pred_P_1 = pred_P_1*condP(feature-1,4); %...P(x=1|y=1)
        end
    end % iterate through every feature until all are multiplied
    
    predP_per_drug(drug,:) = [pred_P_0,pred_P_1];
    if pred_P_0 > pred_P_1
        predC_per_drug = [predC_per_drug,0];
    else
        predC_per_drug = [predC_per_drug,1];
    end
end

num_corr_pred = 0; % number of correctly predicted instances
for drug = 1:num_row
    if X_train(drug,num_col) == predC_per_drug(drug)
        num_corr_pred = num_corr_pred + 1;
    end
end

acc = num_corr_pred/num_row; % accuracy 
        

