*** Settings ***
Resource  resource.robot
Resource  login_resource.robot
Resource  data_resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
No Items Visible
    Go To Home Page
    Set Username  ${test_user_1}
    Set Password  ${test_passwd_1}
    Submit Login Credentials
    Click Element  xpath://*[@id="kirjat"]
    Click Element  xpath://*[@id="podcastit"]
    Click Element  xpath://*[@id="blogit"]
    Click Element  xpath://*[@id="videot"]
    Click Element  xpath://*[@class="btn btn-success"]
    Sleep  1
    Page Should Not Contain  ${test_title}
    Page Should Not Contain  ${test_podcast_title}
    Page Should Not Contain  ${test_blog_title}
    Page Should Not Contain  ${test_video_title}

Books Visible
     Click Element  xpath://*[@id="kirjat"]
     Click Element  xpath://*[@class="btn btn-success"]
     Page Should Contain  ${test_title}

Podcast Visible
    Click Element  xpath://*[@id="kirjat"]
    Click Element  xpath://*[@id="podcastit"]
    Click Element  xpath://*[@class="btn btn-success"]
    Page Should Contain  ${test_podcast_title}

Blog Visible
    Click Element  xpath://*[@id="podcastit"]
    Click Element  xpath://*[@id="blogit"]
    Click Element  xpath://*[@class="btn btn-success"]
    Page Should Contain  ${test_blog_title}

Video Visible
    Click Element  xpath://*[@id="blogit"]
    Click Element  xpath://*[@id="videot"]
    Click Element  xpath://*[@class="btn btn-success"]
    Page Should Contain  ${test_video_title}    

Items Not Marked As Read Visible
    Click Element  xpath://*[@id="kirjat"]
    Click Element  xpath://*[@id="podcastit"]
    Click Element  xpath://*[@id="blogit"]
    Click Element  xpath://*[@id="lukemattomat"]
    Click Element  xpath://*[@class="btn btn-success"]
    sleep  1
    #read stuff shouldn't be visible
    Page Should Not Contain  ${test_title}
    Page Should Not Contain  ${test_episode}
    Page Should Not Contain  ${test_blog_title}
    Page Should Not Contain  ${test_video_title_2}
    #Unread stuff should be visible
    Page Should Contain  ${test_title_2}

Search Items By Full Title
    Go To Home Page
    Set Search Term  ${test_title}
    Click Element  xpath://*[@class="btn btn-success"]
    Page Should Contain  ${test_title}
    Page Should Not Contain  ${test_title_2}

Search Items By Word
    Go To Home Page
    Set Search Term  opiske
    Click Element  xpath://*[@class="btn btn-success"]
    Page Should Contain  ${test_video_title}
    Page Should Contain  ${test_episode_2}
    Page Should Not Contain  ${test_title_2}

Search Items By Nonexistent Read Tip
    Go To Home Page
    Set Search Term  Koira
    Click Element  xpath://*[@class="btn btn-success"]
    Page Should Not Contain  Otsikko:
    Page Should Not Contain  Nimi:

