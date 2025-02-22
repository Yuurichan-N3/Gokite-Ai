import requests
import json
import random
import time
from typing import Dict, List
from datetime import datetime, timedelta
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor

# Setup logging dengan RichHandler, format lebih rapi
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",  # Format: Waktu | Level | Pesan
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler(show_time=False, rich_tracebacks=True)]
)
logger = logging.getLogger("KiteAIAutomation")
console = Console()

# Global Headers
GLOBAL_HEADERS = {
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://agents.testnet.gokite.ai',
    'Referer': 'https://agents.testnet.gokite.ai/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

AI_ENDPOINTS = {
    "https://deployment-hp4y88pxnqxwlmpxllicjzzn.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_Hp4Y88pxNQXwLMPxlLICJZzN",
        "name": "Kite AI Assistant",
        "questions": [
            "Kite AIとは何ですか？",
            "Kite AIは開発者をどのように助けますか？",
            "Kite AIの主な機能は何ですか？",
            "Kite AIのエコシステムを説明できますか？",
            "Kite AIを始めるにはどうすればいいですか？",
            "Kite AIを使う利点は何ですか？",
            "Kite AIは他のAIプラットフォームとどう比較されますか？",
            "Kite AIはどんな問題を解決できますか？",
            "Kite AIのアーキテクチャについて教えてください",
            "Kite AIのユースケースは何ですか？"
        ]
    },
    "https://deployment-nc3y3k7zy6gekszmcsordhu7.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_nC3y3k7zy6gekSZMCSordHu7",
        "name": "Crypto Price Assistant",
        "questions": [
            "ソラナの価格はいくらですか？",
            "ビットコインの現在の価格は何ですか？",
            "イーサリアムの価格トレンドを見せてください",
            "過去24時間の上昇率トップは？",
            "今トレンドのコインはどれですか？",
            "DOTの価格分析を教えてください",
            "AVAXのパフォーマンスはどうですか？",
            "MATICの価格を見せてください",
            "BNBの時価総額はいくらですか？",
            "ADAの価格予測は何ですか？"
        ]
    },
    "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_SoFftlsf9z4fyA3QCHYkaANq",
        "name": "Transaction Analyzer",
        "questions": []
    }
}

def read_wallet_addresses(filename: str = "data.txt") -> List[str]:
    try:
        if not os.path.exists(filename):
            logger.warning(f"{filename} ファイルが見つかりません")
            return []
        with open(filename, 'r') as f:
            addresses = [line.strip() for line in f if line.strip()]
        if not addresses:
            logger.warning(f"{filename} ファイルが空です")
            return []
        logger.info(f"{filename} から {len(addresses)} 個のウォレットアドレスを読み込みました")
        return addresses
    except Exception as e:
        logger.error(f"{filename} ファイルの読み込みエラー: {e}")
        return []

class KiteAIAutomation:
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.MAX_DAILY_POINTS = 200
        self.POINTS_PER_INTERACTION = 10
        self.MAX_DAILY_INTERACTIONS = self.MAX_DAILY_POINTS // self.POINTS_PER_INTERACTION

    def reset_daily_points(self):
        current_time = datetime.now()
        if current_time >= self.next_reset_time:
            logger.info("24時間周期のポイントをリセットします")
            self.daily_points = 0
            self.next_reset_time = current_time + timedelta(hours=24)
            return True
        return False

    def should_wait_for_next_reset(self):
        if self.daily_points >= self.MAX_DAILY_POINTS:
            wait_seconds = (self.next_reset_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                logger.warning(f"1日のポイント上限 ({self.MAX_DAILY_POINTS}) に達しました")
                logger.info(f"次のリセット ({self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}) まで待機します")
                time.sleep(wait_seconds)
                self.reset_daily_points()
            return True
        return False

    def get_recent_transactions(self) -> List[str]:
        logger.info(f"[{self.wallet_address}] 最新のトランザクションを取得中...")
        url = 'https://testnet.kitescan.ai/api/v2/transactions'
        params = {'filter': 'validated'}
        
        headers = GLOBAL_HEADERS.copy()
        headers['accept'] = '*/*'
        
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            hashes = [item['hash'] for item in data.get('items', [])]
            logger.info(f"[{self.wallet_address}] {len(hashes)} 件のトランザクションを取得しました")
            return hashes
        except Exception as e:
            logger.error(f"[{self.wallet_address}] トランザクション取得エラー: {e}")
            return []

    def send_ai_query(self, endpoint: str, message: str) -> str:
        headers = GLOBAL_HEADERS.copy()
        headers['Accept'] = 'text/event-stream'
        
        data = {
            "message": message,
            "stream": True
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=data, stream=True)
            accumulated_response = ""
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        try:
                            json_str = line[6:]
                            if json_str == '[DONE]':
                                break
                            
                            json_data = json.loads(json_str)
                            content = json_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                            if content:
                                accumulated_response += content
                        except json.JSONDecodeError:
                            continue
            
            console.print(f"[cyan][{self.wallet_address}] AI応答:[/cyan] [magenta]{accumulated_response}[/magenta]")
            return accumulated_response.strip()
        except Exception as e:
            logger.error(f"[{self.wallet_address}] AIクエリエラー: {e}")
            return ""

    def report_usage(self, endpoint: str, message: str, response: str) -> bool:
        logger.info(f"[{self.wallet_address}] 使用状況を報告中...")
        url = 'https://quests-usage-dev.prod.zettablock.com/api/report_usage'
        
        headers = GLOBAL_HEADERS.copy()
        
        data = {
            "wallet_address": self.wallet_address,
            "agent_id": AI_ENDPOINTS[endpoint]["agent_id"],
            "request_text": message,
            "response_text": response,
            "request_metadata": {}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"[{self.wallet_address}] 使用状況報告エラー: {e}")
            return False

    def check_stats(self) -> Dict:
        url = f'https://quests-usage-dev.prod.zettablock.com/api/user/{self.wallet_address}/stats'
        
        headers = GLOBAL_HEADERS.copy()
        headers['accept'] = '*/*'
        
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except Exception as e:
            logger.error(f"[{self.wallet_address}] 統計確認エラー: {e}")
            return {}

    def print_stats(self, stats: Dict):
        table = Table(title=f"[{self.wallet_address}] 現在の統計")
        table.add_column("項目", style="cyan")
        table.add_column("値", style="green")
        
        table.add_row("総インタラクション数", str(stats.get('total_interactions', 0)))
        table.add_row("使用したエージェント数", str(stats.get('total_agents_used', 0)))
        table.add_row("初回確認", stats.get('first_seen', 'なし'))
        table.add_row("最終活動", stats.get('last_active', 'なし'))
        
        console.print(table)

    def run(self):
        logger.info(f"[{self.wallet_address}] 24時間制限付きAIインタラクションスクリプトを開始します (Ctrl+Cで終了)")
        console.print(f"[cyan]ウォレットアドレス:[/cyan] [magenta]{self.wallet_address}[/magenta]")
        console.print(f"[cyan]1日のポイント上限:[/cyan] {self.MAX_DAILY_POINTS} ポイント ({self.MAX_DAILY_INTERACTIONS} インタラクション)")
        console.print(f"[cyan]初回リセット時刻:[/cyan] {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        interaction_count = 0
        try:
            while True:
                self.reset_daily_points()
                self.should_wait_for_next_reset()
                
                interaction_count += 1
                console.print(f"\n[cyan][{self.wallet_address}] {'='*50}[/cyan]")
                console.print(f"[magenta]インタラクション #{interaction_count}[/magenta]")
                console.print(f"[cyan]ポイント:[/cyan] {self.daily_points + self.POINTS_PER_INTERACTION}/{self.MAX_DAILY_POINTS} | [cyan]次回リセット:[/cyan] {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                transactions = self.get_recent_transactions()
                AI_ENDPOINTS["https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main"]["questions"] = [
                    f"このトランザクションについてどう思いますか？ {tx}"
                    for tx in transactions
                ]

                endpoint = random.choice(list(AI_ENDPOINTS.keys()))
                question = random.choice(AI_ENDPOINTS[endpoint]["questions"])
                
                console.print(f"\n[cyan]選択したAIアシスタント:[/cyan] [white]{AI_ENDPOINTS[endpoint]['name']}")
                console.print(f"[cyan]エージェントID:[/cyan] [white]{AI_ENDPOINTS[endpoint]['agent_id']}")
                console.print(f"[cyan]質問:[/cyan] [white]{question}")
                
                initial_stats = self.check_stats()
                initial_interactions = initial_stats.get('total_interactions', 0)
                
                response = self.send_ai_query(endpoint, question)
                
                if self.report_usage(endpoint, question, response):
                    logger.info(f"[{self.wallet_address}] 使用状況の報告に成功しました")
                
                final_stats = self.check_stats()
                final_interactions = final_stats.get('total_interactions', 0)
                
                if final_interactions > initial_interactions:
                    logger.info(f"[{self.wallet_address}] インタラクションが正常に記録されました！")
                    self.daily_points += self.POINTS_PER_INTERACTION
                    self.print_stats(final_stats)
                else:
                    logger.warning(f"[{self.wallet_address}] 警告: インタラクションが記録されていない可能性があります")
                
                delay = random.uniform(1, 3)
                with tqdm(total=int(delay * 10), desc=f"[{self.wallet_address}] 待機中", unit="ティック") as pbar:
                    for _ in range(int(delay * 10)):
                        time.sleep(0.1)
                        pbar.update(1)
                
                # Hitungan mundur 3 detik sebelum interaksi berikutnya
                with tqdm(total=30, desc=f"[{self.wallet_address}] 次のインタラクションまで", unit="ティック") as pbar:
                    for _ in range(30):
                        time.sleep(0.1)
                        pbar.update(1)

        except KeyboardInterrupt:
            logger.info(f"[{self.wallet_address}] ユーザーがスクリプトを停止しました")
        except Exception as e:
            logger.error(f"[{self.wallet_address}] エラーが発生しました: {e}")

def process_wallet(wallet_address: str):
    """Fungsi untuk menjalankan automation untuk satu wallet dalam thread."""
    automation = KiteAIAutomation(wallet_address)
    console.print(f"\n[cyan]処理中のウォレット:[/cyan] [magenta]{wallet_address}[/magenta]")
    automation.run()

def main():
    banner = """
╔══════════════════════════════════════════════╗
║           🚀 KITE AI AUTOMATION              ║
║   Automate interactions & earn rewards!      ║
║  Developed by: https://t.me/sentineldiscus   ║
╚══════════════════════════════════════════════╝
    """
    console.print(f"[cyan]{banner}[/cyan]")
    
    addresses = read_wallet_addresses("data.txt")
    
    if not addresses:
        console.print("[red]data.txt にウォレットアドレスが見つかりません。スクリプトを終了します。[/red]")
        return
    
    # Minta input jumlah thread dari pengguna
    while True:
        try:
            num_threads = int(console.input("[yellow]使用するスレッド数を入力してください Jumlah Threads(1-10): [/yellow]"))
            if 1 <= num_threads <= 10:
                break
            else:
                console.print("[red]スレッド数は1から10の間で入力してください。[/red]")
        except ValueError:
            console.print("[red]有効な数字を入力してください。[/red]")
    
    console.print(f"[cyan]選択したスレッド数: {num_threads}[/cyan]")
    
    # Gunakan ThreadPoolExecutor untuk menjalankan wallet secara paralel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(process_wallet, addresses)

if __name__ == "__main__":
    main()
