from enum import Enum
from re import findall, fullmatch
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StrictStr, validator

from .metas.Metas import Speaker, SpeakerInfo


class Mora(BaseModel):
    """
    モーラ（子音＋母音）ごとの情報
    """

    text: str = Field(title="文字")
    consonant: str | None = Field(default=None, title="子音の音素")
    consonant_length: float | None = Field(default=None, title="子音の音長")
    vowel: str = Field(title="母音の音素")
    vowel_length: float = Field(title="母音の音長")
    pitch: float = Field(
        title="音高"
    )  # デフォルト値をつけるとts側のOpenAPIで生成されたコードの型がOptionalになる

    def __hash__(self) -> int:
        items = [
            (k, tuple(v)) if isinstance(v, list) else (k, v)
            for k, v in self.__dict__.items()
        ]
        return hash(tuple(sorted(items)))

    class Config:
        validate_assignment = True


class AccentPhrase(BaseModel):
    """
    アクセント句ごとの情報
    """

    moras: list[Mora] = Field(title="モーラのリスト")
    accent: int = Field(title="アクセント箇所")
    pause_mora: Mora | None = Field(default=None, title="後ろに無音を付けるかどうか")
    is_interrogative: bool = Field(default=False, title="疑問系かどうか")

    def __hash__(self) -> int:
        items = [
            (k, tuple(v)) if isinstance(v, list) else (k, v)
            for k, v in self.__dict__.items()
        ]
        return hash(tuple(sorted(items)))


class AudioQuery(BaseModel):
    """
    音声合成用のクエリ
    """

    accent_phrases: list[AccentPhrase] = Field(title="アクセント句のリスト")
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
    outputSamplingRate: int = Field(title="音声データの出力サンプリングレート")
    outputStereo: bool = Field(title="音声データをステレオ出力するか否か")
    kana: str | None = Field(
        default=None,
        title="読み上げるテキスト (「読みの AquesTalk 風記法テキスト」ではない点で VOICEVOX ENGINE と異なる)",
        description=(
            "読み上げるテキストを指定する。\n"
            "VOICEVOX ENGINE では AquesTalk 風記法テキストが入る読み取り専用フィールドだが (音声合成時には無視される) 、"
            "AivisSpeech Engine では音声合成時に漢字や記号が含まれた通常の読み上げテキストも必要なため、"
            "苦肉の策で読み上げテキスト指定用のフィールドとして転用した。\n"
            "VOICEVOX ENGINE との互換性のため None や空文字列が指定された場合も動作するが、"
            "その場合はアクセント句から自動生成されたひらがな文字列が読み上げテキストになるため、不自然なイントネーションになってしまう。\n"
            "可能な限り kana に通常の読み上げテキストを指定した上で音声合成 API に渡すことを推奨する。"
        ),
    )

    def __hash__(self) -> int:
        items = [
            (k, tuple(v)) if isinstance(v, list) else (k, v)
            for k, v in self.__dict__.items()
        ]
        return hash(tuple(sorted(items)))


class Note(BaseModel):
    """
    音符ごとの情報
    """

    key: int | None = Field(default=None, title="音階")
    frame_length: int = Field(title="音符のフレーム長")
    lyric: str = Field(title="音符の歌詞")


class Score(BaseModel):
    """
    楽譜情報
    """

    notes: list[Note] = Field(title="音符のリスト")


class FramePhoneme(BaseModel):
    """
    音素の情報
    """

    phoneme: str = Field(title="音素")
    frame_length: int = Field(title="音素のフレーム長")


class FrameAudioQuery(BaseModel):
    """
    フレームごとの音声合成用のクエリ
    """

    f0: list[float] = Field(title="フレームごとの基本周波数")
    volume: list[float] = Field(title="フレームごとの音量")
    phonemes: list[FramePhoneme] = Field(title="音素のリスト")
    volumeScale: float = Field(title="全体の音量")
    outputSamplingRate: int = Field(title="音声データの出力サンプリングレート")
    outputStereo: bool = Field(title="音声データをステレオ出力するか否か")


class ParseKanaErrorCode(Enum):
    UNKNOWN_TEXT = "判別できない読み仮名があります: {text}"
    ACCENT_TOP = "句頭にアクセントは置けません: {text}"
    ACCENT_TWICE = "1つのアクセント句に二つ以上のアクセントは置けません: {text}"
    ACCENT_NOTFOUND = "アクセントを指定していないアクセント句があります: {text}"
    EMPTY_PHRASE = "{position}番目のアクセント句が空白です"
    INTERROGATION_MARK_NOT_AT_END = "アクセント句末以外に「？」は置けません: {text}"
    INFINITE_LOOP = "処理時に無限ループになってしまいました...バグ報告をお願いします。"


class ParseKanaError(Exception):
    def __init__(self, errcode: ParseKanaErrorCode, **kwargs: Any) -> None:
        self.errcode = errcode
        self.errname = errcode.name
        self.kwargs = kwargs
        err_fmt: str = errcode.value
        self.text = err_fmt.format(**kwargs)


class ParseKanaBadRequest(BaseModel):
    text: str = Field(title="エラーメッセージ")
    error_name: str = Field(
        title="エラー名",
        description="|name|description|\n|---|---|\n"
        + "\n".join(
            [
                "| {} | {} |".format(err.name, err.value)
                for err in list(ParseKanaErrorCode)
            ]
        ),
    )
    error_args: dict[str, str] = Field(title="エラーを起こした箇所")

    def __init__(self, err: ParseKanaError):
        super().__init__(text=err.text, error_name=err.errname, error_args=err.kwargs)


class MorphableTargetInfo(BaseModel):
    is_morphable: bool = Field(title="指定した話者に対してモーフィングの可否")
    # FIXME: add reason property
    # reason: str | None = Field(default=None, title="is_morphableがfalseである場合、その理由")


class StyleIdNotFoundError(LookupError):
    def __init__(self, style_id: int, *args: object, **kywrds: object) -> None:
        self.style_id = style_id
        super().__init__(f"style_id {style_id} is not found.", *args, **kywrds)


class LibrarySpeaker(BaseModel):
    """
    音声ライブラリに含まれる話者の情報
    """

    speaker: Speaker = Field(title="話者情報")
    speaker_info: SpeakerInfo = Field(title="話者の追加情報")


class BaseLibraryInfo(BaseModel):
    """
    音声ライブラリの情報
    """

    name: str = Field(title="音声ライブラリの名前")
    uuid: str = Field(title="音声ライブラリのUUID")
    version: str = Field(title="音声ライブラリのバージョン")
    download_url: str = Field(title="音声ライブラリのダウンロードURL")
    bytes: int = Field(title="音声ライブラリのバイト数")
    speakers: list[LibrarySpeaker] = Field(title="音声ライブラリに含まれる話者のリスト")


# 今後InstalledLibraryInfo同様に拡張する可能性を考え、モデルを分けている
class DownloadableLibraryInfo(BaseLibraryInfo):
    """
    ダウンロード可能な音声ライブラリの情報
    """

    pass


class InstalledLibraryInfo(BaseLibraryInfo):
    """
    インストール済み音声ライブラリの情報
    """

    uninstallable: bool = Field(title="アンインストール可能かどうか")


USER_DICT_MIN_PRIORITY = 0
USER_DICT_MAX_PRIORITY = 10


class UserDictWord(BaseModel):
    """
    辞書のコンパイルに使われる情報
    """

    surface: str = Field(title="表層形")
    priority: int = Field(
        title="優先度", ge=USER_DICT_MIN_PRIORITY, le=USER_DICT_MAX_PRIORITY
    )
    context_id: int = Field(title="文脈ID", default=1348)
    part_of_speech: str = Field(title="品詞")
    part_of_speech_detail_1: str = Field(title="品詞細分類1")
    part_of_speech_detail_2: str = Field(title="品詞細分類2")
    part_of_speech_detail_3: str = Field(title="品詞細分類3")
    inflectional_type: str = Field(title="活用型")
    inflectional_form: str = Field(title="活用形")
    stem: str = Field(title="原形")
    yomi: str = Field(title="読み")
    pronunciation: str = Field(title="発音")
    accent_type: int = Field(title="アクセント型")
    mora_count: int | None = Field(default=None, title="モーラ数")
    accent_associative_rule: str = Field(title="アクセント結合規則")

    class Config:
        validate_assignment = True

    @validator("surface")
    def convert_to_zenkaku(cls, surface: str) -> str:
        return surface.translate(
            str.maketrans(
                "".join(chr(0x21 + i) for i in range(94)),
                "".join(chr(0xFF01 + i) for i in range(94)),
            )
        )

    @validator("pronunciation", pre=True)
    def check_is_katakana(cls, pronunciation: str) -> str:
        if not fullmatch(r"[ァ-ヴー]+", pronunciation):
            raise ValueError("発音は有効なカタカナでなくてはいけません。")
        sutegana = ["ァ", "ィ", "ゥ", "ェ", "ォ", "ャ", "ュ", "ョ", "ヮ", "ッ"]
        for i in range(len(pronunciation)):
            if pronunciation[i] in sutegana:
                # 「キャット」のように、捨て仮名が連続する可能性が考えられるので、
                # 「ッ」に関しては「ッ」そのものが連続している場合と、「ッ」の後にほかの捨て仮名が連続する場合のみ無効とする
                if i < len(pronunciation) - 1 and (
                    pronunciation[i + 1] in sutegana[:-1]
                    or (
                        pronunciation[i] == sutegana[-1]
                        and pronunciation[i + 1] == sutegana[-1]
                    )
                ):
                    raise ValueError("無効な発音です。(捨て仮名の連続)")
            if pronunciation[i] == "ヮ":
                if i != 0 and pronunciation[i - 1] not in ["ク", "グ"]:
                    raise ValueError(
                        "無効な発音です。(「くゎ」「ぐゎ」以外の「ゎ」の使用)"
                    )
        return pronunciation

    @validator("mora_count", pre=True, always=True)
    def check_mora_count_and_accent_type(
        cls, mora_count: int | None, values: Any
    ) -> int | None:
        if "pronunciation" not in values or "accent_type" not in values:
            # 適切な場所でエラーを出すようにする
            return mora_count

        if mora_count is None:
            rule_others = (
                "[イ][ェ]|[ヴ][ャュョ]|[トド][ゥ]|[テデ][ィャュョ]|[デ][ェ]|[クグ][ヮ]"
            )
            rule_line_i = "[キシチニヒミリギジビピ][ェャュョ]"
            rule_line_u = "[ツフヴ][ァ]|[ウスツフヴズ][ィ]|[ウツフヴ][ェォ]"
            rule_one_mora = "[ァ-ヴー]"
            mora_count = len(
                findall(
                    f"(?:{rule_others}|{rule_line_i}|{rule_line_u}|{rule_one_mora})",
                    values["pronunciation"],
                )
            )

        if not 0 <= values["accent_type"] <= mora_count:
            raise ValueError(
                "誤ったアクセント型です({})。 expect: 0 <= accent_type <= {}".format(
                    values["accent_type"], mora_count
                )
            )
        return mora_count


class PartOfSpeechDetail(BaseModel):
    """
    品詞ごとの情報
    """

    part_of_speech: str = Field(title="品詞")
    part_of_speech_detail_1: str = Field(title="品詞細分類1")
    part_of_speech_detail_2: str = Field(title="品詞細分類2")
    part_of_speech_detail_3: str = Field(title="品詞細分類3")
    # context_idは辞書の左・右文脈IDのこと
    # https://github.com/VOICEVOX/open_jtalk/blob/427cfd761b78efb6094bea3c5bb8c968f0d711ab/src/mecab-naist-jdic/_left-id.def # noqa
    context_id: int = Field(title="文脈ID")
    cost_candidates: list[int] = Field(title="コストのパーセンタイル")
    accent_associative_rules: list[str] = Field(title="アクセント結合規則の一覧")


class WordTypes(str, Enum):
    """
    fastapiでword_type引数を検証する時に使用するクラス
    """

    PROPER_NOUN = "PROPER_NOUN"
    COMMON_NOUN = "COMMON_NOUN"
    VERB = "VERB"
    ADJECTIVE = "ADJECTIVE"
    SUFFIX = "SUFFIX"


class SupportedFeaturesInfo(BaseModel):
    """
    エンジンの機能の情報
    """

    support_adjusting_mora: bool = Field(title="モーラが調整可能かどうか")
    support_adjusting_speed_scale: bool = Field(title="話速が調整可能かどうか")
    support_adjusting_pitch_scale: bool = Field(title="音高が調整可能かどうか")
    support_adjusting_intonation_scale: bool = Field(title="抑揚が調整可能かどうか")
    support_adjusting_volume_scale: bool = Field(title="音量が調整可能かどうか")
    support_adjusting_silence_scale: bool = Field(
        title="前後の無音時間が調節可能かどうか"
    )
    support_interrogative_upspeak: bool = Field(
        title="疑似疑問文に対応しているかどうか"
    )
    support_switching_device: bool = Field(title="CPU/GPUの切り替えが可能かどうか")


class VvlibManifest(BaseModel):
    """
    vvlib(VOICEVOX Library)に関する情報
    """

    manifest_version: StrictStr = Field(title="マニフェストバージョン")
    name: StrictStr = Field(title="音声ライブラリ名")
    version: StrictStr = Field(title="音声ライブラリバージョン")
    uuid: StrictStr = Field(title="音声ライブラリのUUID")
    brand_name: StrictStr = Field(title="エンジンのブランド名")
    engine_name: StrictStr = Field(title="エンジン名")
    engine_uuid: StrictStr = Field(title="エンジンのUUID")


class AivmInfoSpeaker(BaseModel):
    """
    音声合成モデルに含まれる話者の情報
    """

    speaker: Speaker = Field(title="話者情報")
    speaker_info: SpeakerInfo = Field(title="話者の追加情報")


class AivmInfo(BaseModel):
    """
    音声合成モデルの情報
    """

    # model_ 以下を Pydantic の保護対象から除外する
    model_config = ConfigDict(protected_namespaces=())

    name: str = Field(title="音声合成モデルの名前")
    description: str = Field(title="音声合成モデルの説明 (省略時は空文字列になる)")
    model_architecture: str = Field(
        title="音声合成モデルのアーキテクチャ (音声合成技術の種類)"
    )
    uuid: str = Field(title="音声合成モデルの UUID")
    version: str = Field(title="音声合成モデルのバージョン")
    speakers: list[AivmInfoSpeaker] = Field(
        title="音声合成モデルに含まれる話者のリスト"
    )


class AivmManifestSpeakerStyle(BaseModel):
    """
    AIVM (Aivis Voice Model) マニフェストの話者スタイルの定義
    """

    name: StrictStr = Field(title="スタイルの名前")
    id: int = Field(
        title="スタイルの ID (この AIVM ファイル内で一意な 0 から始まる連番で、style_id とは異なる)"
    )


class AivmManifestSpeaker(BaseModel):
    """
    AIVM (Aivis Voice Model) マニフェストの話者の定義
    画像やボイスサンプルは容量が大きいためマニフェストには含まれず、 別途ファイルとして AIVM に格納される
    """

    name: StrictStr = Field(title="話者の名前")
    supported_languages: list[StrictStr] = Field(
        title="話者の対応言語のリスト (ja, en, zh のような ISO 639-1 言語コード)"
    )
    id: int = Field(
        title="話者の ID (この AIVM ファイル内で一意な 0 から始まる連番で、speaker_uuid とは異なる)"
    )
    uuid: StrictStr = Field(title="話者の UUID (speaker_uuid と一致する)")
    version: StrictStr = Field(title="話者のバージョン")
    styles: list[AivmManifestSpeakerStyle] = Field(title="話者スタイルのリスト")


class AivmManifest(BaseModel):
    """
    AIVM (Aivis Voice Model) マニフェストの定義
    """

    # model_ 以下を Pydantic の保護対象から除外する
    model_config = ConfigDict(protected_namespaces=())

    manifest_version: StrictStr = Field(title="AIVM マニフェストのバージョン")
    name: StrictStr = Field(title="音声合成モデルの名前")
    description: StrictStr = Field(
        title="音声合成モデルの説明 (省略時は空文字列になる)"
    )
    model_architecture: StrictStr = Field(
        title="音声合成モデルのアーキテクチャ (音声合成技術の種類)"
    )
    uuid: StrictStr = Field(title="音声合成モデルの UUID")
    version: StrictStr = Field(title="音声合成モデルのバージョン")
    speakers: list[AivmManifestSpeaker] = Field(
        title="音声合成モデルに含まれる話者のリスト"
    )
