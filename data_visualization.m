addpath(genpath('/gpfs/gjor/personal/kirchnerj/src/tools/'))
%%
tab = readtable('data/BolusLoad_nov.csv');
tab.area = tab.cond;
tab.area(tab.area == 4) = 3;
tab.area = categorical(tab.area);
tab.ageFlag = tab. age > 12;
tab.firingrates = 60./tab.IEI;
tab.id = categorical(tab.id);
%%
Gv1 = groupsummary(tab , {'age' , 'area' , 'id'} ,...
                   'mean' , {'amps' , 'durations' , 'rates' , 'firingrates' , 'IEI'},...
                   'IncludeEmptyGroups',false);
%%
lme_amps = fitlme(tab,'amps ~ age*area + (age + area + age:area | id)');
%%
lme_durations = fitlme(tab,'durations ~ age*area + (age + area + age:area | id)');
%%
lme_rates = fitlme(tab,'rates ~ age*area + (age + area + age:area | id)');
%%
lme_firingrates = fitlme(tab,'firingrates ~ age*area + (age + area + age:area | id)');
%%
figure; 
hold on;
scatter(lme_amps.Coefficients.Estimate , 1:length(lme_amps.Coefficients.Estimate) , [] , rgb('black') , 'filled')
plot([lme_amps.Coefficients.Lower , lme_amps.Coefficients.Upper]' , [1:6 ; 1:6] , 'Color' , rgb('black') )
plot([0 , 0] , [0 , 7])
axis square
xlim([-50 , 100]); xticks([-50:50:100])
ylim([0 , 7]); yticks(1:6); yticklabels(lme_amps.Coefficients.Name)
xlabel('amplitude')

%%
figure; 
hold on;
scatter(lme_durations.Coefficients.Estimate , 1:length(lme_durations.Coefficients.Estimate) , [] , rgb('black') , 'filled')
plot([lme_durations.Coefficients.Lower , lme_durations.Coefficients.Upper]' , [1:6 ; 1:6] , 'Color' , rgb('black') )
plot([0 , 0] , [0 , 7])
axis square
xlim([-20 , 20]); xticks([-20:20:20])
ylim([0 , 7]); yticks(1:6); yticklabels(lme_durations.Coefficients.Name)
xlabel('duration')

%%
figure; 
hold on;
scatter(lme_rates.Coefficients.Estimate , 1:length(lme_rates.Coefficients.Estimate) , [] , rgb('black') , 'filled')
plot([lme_rates.Coefficients.Lower , lme_rates.Coefficients.Upper]' , [1:6 ; 1:6] , 'Color' , rgb('black') )
plot([0 , 0] , [0 , 7])
axis square
xlim([-1 , 1.5]); xticks([-1.:0.5:1.5])
ylim([0 , 7]); yticks(1:6); yticklabels(lme_rates.Coefficients.Name)
xlabel('participation')

%%
figure; 
hold on;
scatter(lme_firingrates.Coefficients.Estimate , 1:length(lme_firingrates.Coefficients.Estimate) , [] , rgb('black') , 'filled')
plot([lme_firingrates.Coefficients.Lower , lme_firingrates.Coefficients.Upper]' , [1:6 ; 1:6] , 'Color' , rgb('black') )
plot([0 , 0] , [0 , 7])
axis square
xlim([-5 , 5]); xticks([-5.:5:5])
ylim([0 , 7]); yticks(1:6); yticklabels(lme_firingrates.Coefficients.Name)
xlabel('event rate')

%%
close all
%%
figure;
g = gramm( 'x' ,  Gv1.age , 'y' , Gv1.mean_amps , 'color' , Gv1.area );% , 'color' , augmentSynapses.age);
g.stat_glm('distribution' , 'normal');
g.geom_point;
g.set_point_options('base_size' , 7);
g.axe_property('xlim' , [7 , 17] , 'xtick' , 8:2:16 , ... 
               'ylim' , [15 , 60] , 'ytick' , [15:15:60],... 
                'PlotBoxAspectRatio' , [1 , 1, 1]);
g.set_names('x' , 'age' , 'y' , 'amplitude');
g.no_legend;
g.draw;

%%
figure;
g = gramm( 'x' ,  Gv1.age , 'y' , Gv1.mean_durations , 'color' , Gv1.area );% , 'color' , augmentSynapses.age);
g.stat_glm('distribution' , 'normal');
g.geom_point;
g.set_point_options('base_size' , 7);
g.axe_property('xlim' , [7 , 17] , 'xtick' , 8:2:16 , ... 
               'ylim' , [0 , 15] , 'ytick' , [0:7.5:15],... 
                'PlotBoxAspectRatio' , [1 , 1, 1] );
g.set_names('x' , 'age' , 'y' , 'durations (s)')
g.no_legend;
g.draw;
%%
figure;
g = gramm( 'x' ,  Gv1.age , 'y' , 100*Gv1.mean_rates , 'color' , Gv1.area );% , 'color' , augmentSynapses.age);
g.stat_glm('distribution' , 'normal');
g.geom_point;
g.set_point_options('base_size' , 7);
g.axe_property('xlim' , [7 , 17] , 'xtick' , 8:2:16 , ... 
               'ylim' , [0 , 100] , 'ytick' , [0:50:100],... 
                'PlotBoxAspectRatio' , [1 , 1, 1] );
g.set_names('x' , 'age' , 'y' , 'participation rate (percent)')
g.no_legend;
g.draw;
%%
figure;
g = gramm( 'x' ,  Gv1.age , 'y' , Gv1.mean_IEI , 'color' , Gv1.area );% , 'color' , augmentSynapses.age);
g.stat_glm('distribution' , 'normal' );
g.geom_point;
g.set_point_options('base_size' , 7);
g.axe_property('xlim' , [7 , 17] , 'xtick' , 8:2:16 , ... 
               'ylim' , [0 , 300] , 'ytick' , [0:150:300],... 
                'PlotBoxAspectRatio' , [1 , 1, 1] );
g.set_names('x' , 'age' , 'y' , 'inter event interval (sec)')
g.no_legend;
g.draw;
