# 工作流程

## 3. Github Collaborator工作流程

### 3.1 Collaborator流程

在成为Collaborator之后，`git clone`本仓库到本地

#### 3.1.1 创建远程分支

**在远程仓库中创建一个新的分支**，比如`your_feature_name`，如下两图所示：
![alt text](../resource/attachment/remote_branch_1.png)
![alt text](../resource/attachment/remote_branch_2.png)

#### 3.1.2 本地分支与远程分支关联

### **请注意master分支为我们的主线，请务必务必不要在上面直接开发！！！**
在本地仓库中，使用以下命令 
`git checkout -b your_feature_name --track origin/your_feature_name` 来创建一个本地分支，并与远程分支关联

或者分成两步:
`git checkout -b your_feature_name` 创建本地分支
确保切换到你的分支后，再使用以下命令
`git branch --set-upstream-to=origin/your_feature_name your_feature_name`
### **请务必确定是在你在你的分支下进行开发！！！**

#### 3.1.3 开发与提交

**开发之前，请检查项目主线Master是否有更新**
**在你本地的`master`分支下** `git fetch` && `git pull`来更新本地仓库
**更新之后**, 切换回你的分支，使用`git rebase master`或`git merge master`来合并主线的更新到你的分支(如果有冲突请解决冲突)

**在本地仓库中，开发你的功能**，然后使用`git add`和`git commit`提交你的更改

`git commit`的message请确保准确描述，**并且请不要滥用git commit，不要提交过多commits**
如果想对上一个commit进行补充，请使用`git commit --amend`

**提交前请check是否已经track到正确的远程分支，再git push**
可以用`git branch -vv`来查看本地分支与远程分支的关联情况，**比如**
```
* zhouzhou2 9688362 [origin/zhouzhou2] zhouzhou2 branch fisrt commit
```
zhouzhou2分支已经track到origin/zhouzhou2分支
**或者使用`git push -u origin your_feature_name`**

#### 3.1.4 Pull Request

在github网页端，仓库的`pull request`选项，点击`New pull request`，**compare选择你的分支和base选择Master分支**，创建一个pull request
![alt](../resource/attachment/pull_request.jpg)

### 然后就芜湖恭喜你了，你已经完成了你的任务，等待owner review你的代码吧！


### 3.2 reference

1. 官方文档 https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models 中的共享仓库模型部分
2. [一文带你了解什么Contributor什么是Collaborator](https://blog.csdn.net/qq_41230365/article/details/86766005#:~:text=collaborator%E6%A8%A1%E5%BC%8F%E9%80%82%E5%90%88%E7%94%A8%E4%BA%8E,%E7%9A%84%E6%96%B9%E5%BC%8F%E8%BF%9B%E8%A1%8C%E5%90%88%E4%BD%9C%E5%BC%80%E5%8F%91%E3%80%82)