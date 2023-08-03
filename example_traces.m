close all
allpaths = {'/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/V05 analysis/RL position/Act/V05001.mat',...
            '/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/V05 analysis/V1 position/Act/V05002.mat',...
            '/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/V05 analysis/S1 position/Act/V05006.mat',...
            '/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/RL11 Analysis/RL/Set 1/Act/RL11_003.mat',...
            '/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/RL11 Analysis/V1/Set 1/Act/RL11_001.mat',...
            '/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/RL11 Analysis/S1/Set 1/Act/RL11_002.mat',...
            '/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/RL17  Analysis/RL/Set 1/Act/RL017_003.mat',...
            '/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/RL17  Analysis/V1/Act/RL017_001.mat',...
            '/gpfs/gjor/data/Lab/RAW_DATA/CURLY_2017_2018/NEWER_WITH_MUSCIMOL/Bolus load cal590/RL17  Analysis/S1/Set 1/Act/RL017_008.mat'};
allTitles = {'V05, age 9, RL' , 'V05, age 9, V1' , 'V05, age 9, S1' , ...
             'RL11, age 12, RL' , 'RL11, age 12, V1' , 'RL11, age 12, S1' , ...
             'RL17, age 16, RL' , 'RL17, age 16, V1' , 'RL17, age 16, S1'};
figure;
for xx = 1:9
    subplot(3,3,xx)
    load(allpaths{xx})
    plot(nanmean(act'))
    xlim([0 , 1000]); xticks([0 , 1000]); axis square; box off
    ylim([-5 , 100]); yticks([0 , 50 , 100])
    title(allTitles{xx})
end
