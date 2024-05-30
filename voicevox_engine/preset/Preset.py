"""プリセットのモデルとエラー"""

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError, parse_obj_as

from voicevox_engine.metas.Metas import StyleId


class Preset(BaseModel):
    """
    プリセット情報
    """

    id: int = Field(title="プリセット ID")
    name: str = Field(title="プリセット名")
    speaker_uuid: str = Field(title="話者の UUID")
    style_id: StyleId = Field(title="スタイル ID")
    speedScale: float = Field(
        title="全体の話速",
        description=(
            "全体の話速を 0.5 ~ 2.0 の範囲で指定する (デフォルト: 1.0) 。\n"
            "2.0 で 2 倍速、0.5 で 0.5 倍速になる。"
        ),
    )
    intonationScale: float = Field(
        title="全体のスタイルの強さ (「全体の抑揚」ではない点で VOICEVOX ENGINE と異なる)",
        description=(
            "話者スタイルの声色の強弱を 0.0 ~ 2.0 の範囲で指定する (デフォルト: 1.0) 。\n"
            "値が大きいほどそのスタイルに近い抑揚がついた声になる。\n"
            "例えば話者スタイルが「うれしい」なら、値が大きいほどより嬉しそうな明るい話し方になる。\n"
            "一方スタイルによっては値を大きくしすぎると不自然な棒読みボイスになりがちなので、適宜調整が必要。\n"
            "全スタイルの平均であるノーマルスタイルには指定できない (値にかかわらず無視される) 。"
        ),
    )
    tempoDynamicsScale: float = Field(
        default=1.0,
        title="全体のテンポの緩急 (AivisSpeech Engine 固有のフィールド)",
        description=(
            "話す速さの緩急の強弱を 0.0 ~ 2.0 の範囲で指定する (デフォルト: 1.0) 。\n"
            "値が大きいほどより早口で生っぽい抑揚がついた声になる。\n"
            "VOICEVOX ENGINE との互換性のため、未指定時はデフォルト値が適用される。"
        ),
    )
    pitchScale: float = Field(
        title="全体の音高",
        description=(
            "全体の音高を -0.15 ~ 0.15 の範囲で指定する (デフォルト: 0.0) 。\n"
            "値が大きいほど高い声になる。\n"
            "VOICEVOX ENGINE と異なり、この値を 0.0 から変更すると音質が劣化するため注意が必要。"
        ),
    )
    volumeScale: float = Field(
        title="全体の音量",
        description=(
            "全体の音量を 0.0 ~ 2.0 の範囲で指定する (デフォルト: 1.0) 。\n"
            "値が大きいほど大きな声になる。"
        ),
    )
    prePhonemeLength: float = Field(title="音声の前の無音時間 (秒)")
    postPhonemeLength: float = Field(title="音声の後の無音時間 (秒)")


class PresetInputError(Exception):
    """受け入れ不可能な入力値に起因するエラー"""

    pass


class PresetInternalError(Exception):
    """プリセットマネージャーに起因するエラー"""

    pass


class PresetManager:
    """
    プリセットの管理

    プリセットはAudioQuery全体パラメータ（話速・音高・抑揚・音量・無音長）のデフォルト値セットである。
    YAMLファイルをSSoTとする簡易データベース方式により、プリセットの管理をおこなう。
    """

    def __init__(self, preset_path: Path):
        """プリセットの設定ファイルへのパスからプリセットマネージャーを生成する"""
        self.presets: list[Preset] = []  # 全プリセットのキャッシュ
        self.last_modified_time = 0.0
        self.preset_path = preset_path

    def _refresh_cache(self) -> None:
        """プリセットの設定ファイルの最新状態をキャッシュへ反映する"""

        # データベース更新の確認（タイムスタンプベース）
        try:
            _last_modified_time = self.preset_path.stat().st_mtime
            if _last_modified_time == self.last_modified_time:
                # 更新無し
                return
        except OSError:
            raise PresetInternalError("プリセットの設定ファイルが見つかりません")

        # データベースの読み込み
        with open(self.preset_path, mode="r", encoding="utf-8") as f:
            obj = yaml.safe_load(f)
            if obj is None:
                raise PresetInternalError("プリセットの設定ファイルが空の内容です")
        try:
            _presets = parse_obj_as(list[Preset], obj)
        except ValidationError:
            raise PresetInternalError("プリセットの設定ファイルにミスがあります")

        # 全idの一意性をバリデーション
        if len([preset.id for preset in _presets]) != len(
            {preset.id for preset in _presets}
        ):
            raise PresetInternalError("プリセットのidに重複があります")

        # キャッシュを更新する
        self.presets = _presets
        self.last_modified_time = _last_modified_time

    def add_preset(self, preset: Preset) -> int:
        """新規プリセットを追加し、その ID を取得する。"""

        # データベース更新の反映
        self._refresh_cache()

        # 新規プリセットID の発行。IDが0未満、または存在するIDなら新規IDを発行
        if preset.id < 0 or preset.id in {preset.id for preset in self.presets}:
            preset.id = max([preset.id for preset in self.presets]) + 1
        # 新規プリセットの追加
        self.presets.append(preset)

        # 変更の反映。失敗時はリバート。
        try:
            self._write_on_file()
        except Exception as err:
            self.presets.pop()
            if isinstance(err, FileNotFoundError):
                raise PresetInternalError("プリセットの設定ファイルが見つかりません")
            else:
                raise err

        return preset.id

    def load_presets(self) -> list[Preset]:
        """全てのプリセットを取得する"""

        # データベース更新の反映
        self._refresh_cache()

        return self.presets

    def update_preset(self, preset: Preset) -> int:
        """指定されたプリセットを更新し、その ID を取得する。"""

        # データベース更新の反映
        self._refresh_cache()

        # 対象プリセットの検索
        prev_preset: tuple[int, Preset | None] = (-1, None)
        for i in range(len(self.presets)):
            if self.presets[i].id == preset.id:
                prev_preset = (i, self.presets[i])
                self.presets[i] = preset
                break
        else:
            raise PresetInputError("更新先のプリセットが存在しません")

        # 変更の反映。失敗時はリバート。
        try:
            self._write_on_file()
        except Exception as err:
            self.presets[prev_preset[0]] = prev_preset[1]
            if isinstance(err, FileNotFoundError):
                raise PresetInternalError("プリセットの設定ファイルが見つかりません")
            else:
                raise err

        return preset.id

    def delete_preset(self, id: int) -> int:
        """ID で指定されたプリセットを削除し、その ID を取得する。"""

        # データベース更新の反映
        self._refresh_cache()

        # 対象プリセットの検索
        buf = None
        buf_index = -1
        for i in range(len(self.presets)):
            if self.presets[i].id == id:
                buf = self.presets.pop(i)
                buf_index = i
                break
        else:
            raise PresetInputError("削除対象のプリセットが存在しません")

        # 変更の反映。失敗時はリバート。
        try:
            self._write_on_file()
        except FileNotFoundError:
            self.presets.insert(buf_index, buf)
            raise PresetInternalError("プリセットの設定ファイルが見つかりません")

        return id

    def _write_on_file(self) -> None:
        """プリセット情報のファイル（簡易データベース）書き込み"""
        with open(self.preset_path, mode="w", encoding="utf-8") as f:
            yaml.safe_dump(
                [preset.model_dump() for preset in self.presets],
                f,
                allow_unicode=True,
                sort_keys=False,
            )
