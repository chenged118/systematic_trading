#!/bin/bash

# 判斷是否輸入 commit 訊息
if [ -z "$1" ]; then
  echo "❗ 請輸入 commit 訊息，例如："
  echo "    ./git_push.sh \"Fix bug in strategy\""
  exit 1
fi

# 加入所有變更
git add .

# 建立 commit
git commit -m "$1"

# Push 到 GitHub（origin）
echo "🚀 Push to GitHub..."
git push github main

# Push 到 GitLab（gitlab）
echo "🚀 Push to GitLab..."
git push gitlab main

echo "✅ 推送完成"